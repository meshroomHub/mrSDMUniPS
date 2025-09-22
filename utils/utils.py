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

def update_intrinsics_after_rotation_and_crop(intrinsic, rotation_applied, crop_bbox):
    """
    Update camera intrinsics after rotation and cropping.
    
    Args:
        intrinsic: Camera intrinsic object
        rotation_applied: Rotation angle applied (0 or 90 degrees)
        crop_bbox: (x, y, width, height) of the crop
        
    Returns:
        Updated intrinsic parameters
    """
    from pyalicevision import camera, numeric
    
    # Cast to Pinhole camera model
    cam = camera.Pinhole.cast(intrinsic)
    if cam is None:
        return intrinsic  # Can't update non-pinhole models
    
    # Apply crop offset
    if crop_bbox:
        crop_x, crop_y, new_width, new_height = crop_bbox
    
        # Get current principal point
        pp = cam.getPrincipalPoint()
        pp_x = numeric.getX(pp)
        pp_y = numeric.getY(pp)
        logging.debug(f"Original principal point: ({pp_x}, {pp_y})")

        # Adjust principal point
        new_ppx = pp_x - crop_x
        new_ppy = pp_y - crop_y
        logging.debug(f"Adjusted principal point: ({new_ppx}, {new_ppy})")

        # Get new offset
        new_px = new_width / 2 - new_ppx
        new_py = new_height / 2 - new_ppy
        logging.debug(f"New offset: ({new_px}, {new_py})")
        
        # Set new offset
        cam.setOffset(np.array([new_px, new_py]))

        # Set new image size
        cam.setWidth(new_width)
        cam.setHeight(new_height)
        
    return intrinsic