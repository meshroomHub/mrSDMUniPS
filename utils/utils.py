import cv2
import numpy as np
import os
from pathlib import Path
from pyalicevision import sfmData, sfmDataIO, image as aliceImage
import logging

def ensure_landscape_orientation(image):
    """
    Ensure image is in landscape orientation (width > height).
    Returns the image and rotation info.
    """
    height, width = image.shape[:2]
    
    if height > width:
        # Rotate 90 degrees clockwise to make it landscape
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        rotation_applied = 90
    else:
        # Already landscape or square
        rotated_image = image
        rotation_applied = 0
    
    return rotated_image, rotation_applied

def estimate_common_bbox_from_masks(mask_paths, target_size=None):
    """
    Estimate a common bounding box from multiple mask files.
    
    Args:
        mask_paths: List of paths to mask files
        target_size: Optional tuple (width, height) to constrain the bbox
        
    Returns:
        bbox: (x, y, width, height) or None if no valid masks found
    """
    if not mask_paths:
        return None
    
    valid_masks = []
    original_size = None
    
    for mask_path in mask_paths:
        if not os.path.exists(mask_path):
            continue
            
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            continue
            
        # Ensure landscape orientation for mask too
        mask, _ = ensure_landscape_orientation(mask)
        
        if original_size is None:
            original_size = (mask.shape[1], mask.shape[0])  # (width, height)
        elif (mask.shape[1], mask.shape[0]) != original_size:
            # Resize mask to match the first valid mask size
            mask = cv2.resize(mask, original_size)
        
        valid_masks.append(mask)
    
    if not valid_masks:
        return None
    
    # Combine all masks (union)
    combined_mask = np.zeros_like(valid_masks[0])
    for mask in valid_masks:
        combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    # Find bounding box of the combined mask
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Get bounding box of all contours
    x_min, y_min = float('inf'), float('inf')
    x_max, y_max = -float('inf'), -float('inf')
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)
    
    if x_min == float('inf'):
        return None
    
    bbox_width = int(x_max - x_min)
    bbox_height = int(y_max - y_min)
    
    # Apply target size constraints if specified
    if target_size:
        target_width, target_height = target_size
        
        # Center the bbox and adjust to target size
        center_x = x_min + bbox_width // 2
        center_y = y_min + bbox_height // 2
        
        x_min = max(0, center_x - target_width // 2)
        y_min = max(0, center_y - target_height // 2)
        
        # Ensure we don't exceed image boundaries
        x_min = min(x_min, original_size[0] - target_width)
        y_min = min(y_min, original_size[1] - target_height)
        
        bbox_width = target_width
        bbox_height = target_height
    
    return (int(x_min), int(y_min), int(bbox_width), int(bbox_height))

def update_intrinsics_after_rotation_and_crop(intrinsic, rotation_applied, crop_bbox, original_size):
    """
    Update camera intrinsics after rotation and cropping.
    
    Args:
        intrinsic: Camera intrinsic object
        rotation_applied: Rotation angle applied (0 or 90 degrees)
        crop_bbox: (x, y, width, height) of the crop
        original_size: (width, height) of the original image
        
    Returns:
        Updated intrinsic parameters
    """
    from pyalicevision import camera, numeric
    
    # Cast to Pinhole camera model
    cam = camera.Pinhole.cast(intrinsic)
    if cam is None:
        return intrinsic  # Can't update non-pinhole models
    
    if rotation_applied == 90:
        # After 90-degree clockwise rotation:
        # - Image dimensions swap: (W, H) -> (H, W)
        # - Principal point transforms: (px, py) -> (H - py, px)
        
        original_width, original_height = original_size
        
        # Get current offset (principal point)
        offset = cam.getOffset()
        current_px = -numeric.getX(offset)  # Note: offset is negative of principal point
        current_py = numeric.getY(offset)
        
        # Calculate new principal point after rotation
        new_px = original_height - current_py
        new_py = current_px
        
        # Set new offset (remember to negate px)
        new_offset = numeric.Vec2(-new_px, new_py)
        cam.setOffset(new_offset)
    
    # Apply crop offset
    if crop_bbox:
        crop_x, crop_y, _, _ = crop_bbox
        
        # Get current offset
        offset = cam.getOffset()
        current_px = -numeric.getX(offset)
        current_py = numeric.getY(offset)
        
        # Apply crop offset
        new_px = current_px - crop_x
        new_py = current_py - crop_y
        
        # Set new offset
        new_offset = numeric.Vec2(-new_px, new_py)
        cam.setOffset(new_offset)
    
    return intrinsic

def preprocess_images_and_sfmdata(input_sfm_path, output_sfm_path, output_images_dir, 
                                mask_paths=None, enable_cropping=True, target_crop_size=None,
                                logger=None):
    """
    Preprocess images and SfMData: ensure landscape orientation and optionally crop based on masks.
    
    Args:
        input_sfm_path: Path to input SfMData file
        output_sfm_path: Path to output SfMData file
        output_images_dir: Directory to save processed images
        mask_paths: List of mask file paths for bbox estimation
        enable_cropping: Whether to enable cropping
        target_crop_size: Optional (width, height) for crop size
        logger: Logger instance
    
    Returns:
        dict with processing results
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    try:
        # Load input SfMData
        input_sfm_data = sfmData.SfMData()
        if not sfmDataIO.load(input_sfm_data, input_sfm_path, sfmDataIO.ALL):
            raise RuntimeError(f"Failed to load input SfMData file: {input_sfm_path}")
        
        # Create output directory
        Path(output_images_dir).mkdir(parents=True, exist_ok=True)
        
        # Estimate common bbox if cropping is enabled and masks are provided
        common_bbox = None
        if enable_cropping and mask_paths:
            logger.info(f"Estimating common bbox from {len(mask_paths)} masks")
            common_bbox = estimate_common_bbox_from_masks(mask_paths, target_crop_size)
            if common_bbox:
                logger.info(f"Common bbox estimated: {common_bbox}")
            else:
                logger.warning("Could not estimate common bbox from masks")
        
        # Process each view
        views = input_sfm_data.getViews()
        processed_count = 0
        rotation_stats = {"rotated": 0, "unchanged": 0}
        
        for view_id, view in views.items():
            image_path = view.getImage().getImagePath()
            
            if not os.path.exists(image_path):
                logger.warning(f"Image not found: {image_path}")
                continue
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                logger.warning(f"Could not load image: {image_path}")
                continue
            
            original_size = (img.shape[1], img.shape[0])  # (width, height)
            
            # Ensure landscape orientation
            processed_img, rotation_applied = ensure_landscape_orientation(img)
            
            if rotation_applied > 0:
                rotation_stats["rotated"] += 1
                logger.info(f"Rotated image {Path(image_path).name} by {rotation_applied} degrees")
            else:
                rotation_stats["unchanged"] += 1
            
            # Apply cropping if enabled and bbox is available
            if enable_cropping and common_bbox:
                crop_x, crop_y, crop_w, crop_h = common_bbox
                processed_img = processed_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                logger.info(f"Cropped image {Path(image_path).name} to {crop_w}x{crop_h}")
            
            # Save processed image
            output_image_path = Path(output_images_dir) / Path(image_path).name
            cv2.imwrite(str(output_image_path), processed_img)
            
            # Update view with new image path
            view.getImage().setImagePath(str(output_image_path))
            
            # Update image dimensions
            new_height, new_width = processed_img.shape[:2]
            view.getImage().setWidth(new_width)
            view.getImage().setHeight(new_height)
            
            # Update intrinsics
            intrinsic_id = view.getIntrinsicId()
            if input_sfm_data.getIntrinsics().count(intrinsic_id) > 0:
                intrinsic = input_sfm_data.getIntrinsics()[intrinsic_id]
                updated_intrinsic = update_intrinsics_after_rotation_and_crop(
                    intrinsic, rotation_applied, common_bbox if enable_cropping else None, original_size
                )
                # The intrinsic object is modified in place
                logger.info(f"Updated intrinsics for view {view_id} (intrinsic_id: {intrinsic_id})")
            
            processed_count += 1
        
        # Save updated SfMData
        if not sfmDataIO.save(input_sfm_data, output_sfm_path, sfmDataIO.ALL):
            raise RuntimeError(f"Failed to save updated SfMData to: {output_sfm_path}")
        
        logger.info(f"Preprocessing completed: {processed_count} images processed")
        logger.info(f"Rotation stats: {rotation_stats['rotated']} rotated, {rotation_stats['unchanged']} unchanged")
        
        return {
            "success": True,
            "processed_count": processed_count,
            "rotation_stats": rotation_stats,
            "common_bbox": common_bbox,
            "output_sfm_path": output_sfm_path,
            "output_images_dir": output_images_dir
        }
    
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        return {
            "success": False,
            "error": str(e)
        }