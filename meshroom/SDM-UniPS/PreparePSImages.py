__version__ = "0.1"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
import os
from pathlib import Path

class PreparePSImages(desc.Node):
    size = desc.DynamicNodeSize("inputPath")
    
    category = "Photometric Stereo"
    documentation = """
Prepare Images for Photometric Stereo

This node preprocesses images for photometric stereo processing by:
1. Organizing images by pose for photometric stereo algorithms
2. Extracting and processing masks from alpha channels or external files
3. Optionally ensuring landscape orientation
4. Optionally cropping images based on mask bounding boxes
5. Creating the data structure expected by photometric stereo algorithms

The output includes both a preprocessed SfMData file and organized image folders
ready for photometric stereo processing.
"""

    inputs = [
        desc.File(
            name="inputPath",
            label="Input SfMData",
            description="Input SfMData file containing images and poses.",
            value="",
        ),
        desc.File(
            name="maskPath",
            label="Mask Folder Path", 
            description="Path to a folder containing masks or to a single mask file.",
            value="",
        ),
        desc.BoolParam(
            name="enableLandscapeRotation",
            label="Enable Landscape Rotation",
            description="Rotate images to landscape orientation (width > height) without updating intrinsics.",
            value=True,
        ),
        desc.BoolParam(
            name="enableCropping",
            label="Enable Cropping",
            description="Enable cropping based on mask bounding box estimation.",
            value=False,
        ),
        desc.IntParam(
            name="targetCropWidth",
            label="Target Crop Width",
            description="Target width for cropping (0 = automatic based on masks).",
            value=0,
            range=(0, 4096, 1),
            advanced=True,
        ),
        desc.IntParam(
            name="targetCropHeight", 
            label="Target Crop Height",
            description="Target height for cropping (0 = automatic based on masks).",
            value=0,
            range=(0, 4096, 1),
            advanced=True,
        ),
        desc.StringParam(
            name="dataFolderSuffix",
            label="Data Folder Suffix",
            description="Suffix for data folders (e.g., '.data' for pose_0.data).",
            value=".data",
            advanced=True,
        ),
        desc.StringParam(
            name="imagePrefix",
            label="Image Prefix",
            description="Prefix for organized images (e.g., 'L' for L000.jpg, L001.jpg).",
            value="L",
            advanced=True,
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level (fatal, error, warning, info, debug, trace).",
            values=VERBOSE_LEVEL,
            value="info",
        ),
    ]

    outputs = [
        desc.File(
            name="outputSfmData",
            label="Output SfMData",
            description="Preprocessed SfMData file with organized image information.",
            value="{nodeCacheFolder}/sfmData.sfm",
        ),
        desc.File(
            name="outputDataFolder",
            label="Output Data Folder",
            description="Folder containing organized images and masks for photometric stereo.",
            value="{nodeCacheFolder}/ps_data",
        ),
    ]

    def processChunk(self, chunk):
        """
        Process the photometric stereo data preparation.
        """
        try:
            import shutil
            import cv2
            import numpy as np
            from pyalicevision import sfmData, sfmDataIO
            from utils.utils import ensure_landscape_orientation, estimate_common_bbox_from_masks, update_intrinsics_after_rotation_and_crop
            
            chunk.logManager.start(chunk.node.verboseLevel.value)
            
            if not chunk.node.inputPath.value:
                raise RuntimeError("No input SfMData file provided")
            
            # Load input SfMData
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputPath.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputPath.value}")
            
            # Create output directories
            output_data_dir = Path(chunk.node.outputDataFolder.value)
            output_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Collect mask paths for preprocessing if cropping is enabled
            mask_paths = []
            alpha_mask_paths = []
            common_bbox = None
            
            if chunk.node.enableCropping.value:
                # Collect external mask files if provided
                if chunk.node.maskPath.value:
                    mask_path = Path(chunk.node.maskPath.value)
                    
                    if mask_path.is_dir():
                        # Look for mask files in directory
                        for ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
                            mask_paths.extend(list(mask_path.glob(f'*{ext}')))
                            mask_paths.extend(list(mask_path.glob(f'*{ext.upper()}')))
                    elif mask_path.is_file():
                        # Single mask file
                        mask_paths = [mask_path]
                
                # Also collect alpha channels from representative images (viewId == poseId)
                views = input_sfm_data.getViews()
                for view_id, view in views.items():
                    pose_id = view.getPoseId()
                    
                    # Only check representative images (viewId == poseId)
                    if view_id == pose_id:
                        image_path = view.getImage().getImagePath()
                        
                        if os.path.exists(image_path):
                            # Check if image has alpha channel
                            img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                            if img is not None and len(img.shape) == 3 and img.shape[2] == 4:
                                # Extract alpha channel and save as temporary mask for preprocessing
                                alpha_mask = img[:, :, 3]
                                temp_mask_path = Path(chunk.node.outputDataFolder.value) / f"temp_alpha_mask_{pose_id}.png"
                                temp_mask_path.parent.mkdir(parents=True, exist_ok=True)
                                cv2.imwrite(str(temp_mask_path), alpha_mask)
                                alpha_mask_paths.append(temp_mask_path)
                                chunk.logger.debug(f"Extracted alpha channel from representative image for pose {pose_id}")
                
                # Combine external masks and alpha channel masks
                all_mask_paths = mask_paths + alpha_mask_paths
                
                if all_mask_paths:
                    chunk.logger.info(f"Collected {len(mask_paths)} external masks and {len(alpha_mask_paths)} alpha channel masks for preprocessing")
                    
                    # Determine target crop size
                    target_crop_size = None
                    if (chunk.node.targetCropWidth.value > 0 and chunk.node.targetCropHeight.value > 0):
                        target_crop_size = (chunk.node.targetCropWidth.value, chunk.node.targetCropHeight.value)
                    
                    # Estimate common bbox if cropping is enabled and masks are provided
                    chunk.logger.info(f"Estimating common bbox from {len(all_mask_paths)} masks")
                    common_bbox = estimate_common_bbox_from_masks(all_mask_paths, target_crop_size)
                    if common_bbox:
                        chunk.logger.info(f"Common bbox estimated: {common_bbox}")
                    else:
                        chunk.logger.warning("Could not estimate common bbox from masks")
                else:
                    chunk.logger.info("No masks found for cropping")

                # Clean up temporary alpha mask files
                for temp_mask_path in alpha_mask_paths:
                    try:
                        os.remove(temp_mask_path)
                    except OSError:
                        pass  # Ignore cleanup errors
            else:
                chunk.logger.info("Cropping disabled")
            
            # Get views per pose ID
            views_per_pose_id = {}
            views = input_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                if pose_id not in views_per_pose_id:
                    views_per_pose_id[pose_id] = []
                views_per_pose_id[pose_id].append(view_id)
            
            # Create updated SfMData with new image paths
            updated_sfm_data = input_sfm_data
            processed_count = 0
            updated_intrinsics = set()  # Track which intrinsics have been updated
            
            # Process each pose separately
            for pose_id, view_ids in views_per_pose_id.items():
                chunk.logger.info(f"Processing Pose ID: {pose_id}")
                
                # Create pose directory
                pose_dir = output_data_dir / f"pose_{pose_id}{chunk.node.dataFolderSuffix.value}"
                pose_dir.mkdir(parents=True, exist_ok=True)
                
                # Get image list for this pose
                image_list = []
                for view_id in view_ids:
                    view = input_sfm_data.getView(view_id)
                    image_path = view.getImage().getImagePath()
                    image_list.append((view_id, image_path))
                
                if len(image_list) < 1:
                    chunk.logger.warning(f"Empty image list for pose {pose_id}, skipping.")
                    continue
                
                # Process images with photometric stereo naming
                prefix = chunk.node.imagePrefix.value
                alpha_mask = None
                alpha_mask_found = False
                rotation_applied = 0
                original_size = None
                
                for i, (view_id, image_path) in enumerate(image_list):
                    if not os.path.isfile(image_path):
                        chunk.logger.warning(f"Image file not found: {image_path}")
                        continue
                    
                    src_path = Path(image_path)
                    # Create filename with prefix and zero-padded index
                    dst_filename = f"{prefix}{i:03d}{src_path.suffix}"
                    dst_path = pose_dir / dst_filename
                    
                    # Load and preprocess image
                    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
                    if img is None:
                        chunk.logger.warning(f"Could not read image: {image_path}")
                        continue
                    
                    # Store original size for intrinsic update (only for first representative image)
                    if view_id == pose_id and original_size is None:
                        if len(img.shape) == 3 and img.shape[2] == 4:
                            original_size = (img.shape[1], img.shape[0])  # (width, height) without alpha
                        else:
                            original_size = (img.shape[1], img.shape[0])  # (width, height)
                    
                    # Handle alpha channel extraction (only for representative images)
                    pose_id_current = updated_sfm_data.getView(view_id).getPoseId()
                    if view_id == pose_id_current and len(img.shape) == 3 and img.shape[2] == 4:
                        chunk.logger.debug(f"Alpha channel detected in {src_path.name}")
                        
                        # Extract alpha channel as mask (first image sets the mask)
                        if not alpha_mask_found:
                            alpha_mask = img[:, :, 3]  # Extract alpha channel
                            alpha_mask_found = True
                            chunk.logger.debug(f"Using alpha channel from {src_path.name} as mask for pose {pose_id}")
                        
                        # Remove alpha channel and keep only RGB
                        img = img[:, :, :3]  # Keep only RGB channels
                    
                    # Apply preprocessing: ensure landscape orientation (simple rotation, no intrinsic update)
                    processed_img = img
                    if chunk.node.enableLandscapeRotation.value:
                        processed_img, current_rotation = ensure_landscape_orientation(img)
                        if view_id == pose_id:  # Store rotation info from representative image
                            rotation_applied = current_rotation
                        if current_rotation > 0:
                            chunk.logger.debug(f"Rotated image {src_path.name} by {current_rotation} degrees")
                    
                    # Apply cropping if enabled and bbox is available
                    if chunk.node.enableCropping.value and common_bbox:
                        crop_x, crop_y, crop_w, crop_h = common_bbox
                        processed_img = processed_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                        chunk.logger.debug(f"Cropped image {src_path.name} to {crop_w}x{crop_h}")
                    
                    # Save processed image
                    cv2.imwrite(str(dst_path), processed_img)
                    chunk.logger.debug(f"Processed and saved {src_path.name} -> {dst_filename}")
                    
                    # Update SfMData with new image path and dimensions
                    view = updated_sfm_data.getView(view_id)
                    view.getImage().setImagePath(str(dst_path))
                    
                    # Update image dimensions if cropping was applied
                    if chunk.node.enableCropping.value and common_bbox:
                        new_height, new_width = processed_img.shape[:2]
                        view.getImage().setWidth(new_width)
                        view.getImage().setHeight(new_height)
                        chunk.logger.debug(f"Updated image dimensions for {src_path.name}: {new_width}x{new_height}")
                    
                    processed_count += 1
                
                # Handle mask: alpha channel takes priority, then external mask
                mask_copied = False
                
                # First, process and save alpha channel mask if found
                if alpha_mask_found and alpha_mask is not None:
                    # Apply same preprocessing to alpha mask
                    processed_mask = alpha_mask
                    if chunk.node.enableLandscapeRotation.value and rotation_applied > 0:
                        processed_mask, _ = ensure_landscape_orientation(alpha_mask)
                    if chunk.node.enableCropping.value and common_bbox:
                        crop_x, crop_y, crop_w, crop_h = common_bbox
                        processed_mask = processed_mask[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                    
                    mask_path = pose_dir / "mask.png"
                    cv2.imwrite(str(mask_path), processed_mask)
                    chunk.logger.debug(f"Saved processed alpha channel mask for pose {pose_id}")
                    mask_copied = True
                
                # If no alpha mask and external mask path provided, try external masks
                elif chunk.node.maskPath.value:
                    mask_to_process = None
                    mask_source = None
                    
                    if os.path.isdir(chunk.node.maskPath.value):
                        # Look for pose-specific mask
                        mask_patterns = [
                            f"pose_{pose_id}_mask.png",
                            f"{pose_id}_mask.png", 
                            f"mask_{pose_id}.png",
                            f"{pose_id}.png",
                            "mask.png"  # Generic mask
                        ]
                        for pattern in mask_patterns:
                            mask_file = os.path.join(chunk.node.maskPath.value, pattern)
                            if os.path.isfile(mask_file):
                                mask_img = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)
                                if mask_img is not None:
                                    mask_to_process = mask_img
                                    mask_source = pattern
                                    break
                        
                        if mask_to_process is None:
                            chunk.logger.debug(f"No external mask found for pose {pose_id} in {chunk.node.maskPath.value}")
                            
                    elif os.path.isfile(chunk.node.maskPath.value):
                        # Single mask file for all poses
                        mask_img = cv2.imread(chunk.node.maskPath.value, cv2.IMREAD_GRAYSCALE)
                        if mask_img is not None:
                            mask_to_process = mask_img
                            mask_source = "global external mask"
                    else:
                        chunk.logger.debug(f"External mask path is neither a directory nor a file: {chunk.node.maskPath.value}")
                    
                    # Process the external mask if found
                    if mask_to_process is not None:
                        processed_mask = mask_to_process
                        
                        # Apply the same preprocessing transformations as the images
                        if chunk.node.enableLandscapeRotation.value and rotation_applied > 0:
                            processed_mask, _ = ensure_landscape_orientation(mask_to_process)
                            chunk.logger.debug(f"Rotated mask for pose {pose_id} by {rotation_applied} degrees")
                        
                        if chunk.node.enableCropping.value and common_bbox:
                            crop_x, crop_y, crop_w, crop_h = common_bbox
                            processed_mask = processed_mask[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                            chunk.logger.debug(f"Cropped mask for pose {pose_id} to {crop_w}x{crop_h}")
                        
                        mask_path = pose_dir / "mask.png"
                        cv2.imwrite(str(mask_path), processed_mask)
                        chunk.logger.debug(f"Copied and processed {mask_source} for pose {pose_id}")
                        mask_copied = True

                if not mask_copied:
                    chunk.logger.debug(f"No mask used for pose {pose_id}")

                chunk.logger.info(f"Prepared {len(image_list)} images for pose {pose_id} in {pose_dir}")

                # Update intrinsics only once per intrinsic_id (after processing all images for this pose)
                if chunk.node.enableCropping.value and common_bbox and original_size:
                    # Get representative view for this pose
                    representative_view = updated_sfm_data.getView(pose_id)
                    intrinsic_id = representative_view.getIntrinsicId()
                    
                    # Only update if this intrinsic hasn't been updated yet
                    if intrinsic_id not in updated_intrinsics:
                        if updated_sfm_data.getIntrinsics().count(intrinsic_id) > 0:
                            intrinsic = updated_sfm_data.getIntrinsics()[intrinsic_id]
                            
                            # Update intrinsics considering both rotation and crop
                            updated_intrinsic = update_intrinsics_after_rotation_and_crop(
                                intrinsic, rotation_applied, common_bbox
                            )
                            
                            # Mark this intrinsic as updated
                            updated_intrinsics.add(intrinsic_id)
                            chunk.logger.info(f"Updated intrinsics for intrinsic_id {intrinsic_id} (used by pose {pose_id})")
                        else:
                            chunk.logger.warning(f"Intrinsic {intrinsic_id} not found for pose {pose_id}")

            # Save updated SfMData
            if not sfmDataIO.save(updated_sfm_data, chunk.node.outputSfmData.value, sfmDataIO.ALL):
                chunk.logger.warning(f"Failed to save updated SfMData to: {chunk.node.outputSfmData.value}")
            else:
                chunk.logger.debug(f"Updated SfMData saved to: {chunk.node.outputSfmData.value}")

            chunk.logger.info(f"Photometric stereo data preparation completed")
            chunk.logger.info(f"Processed {processed_count} images total")
            chunk.logger.info(f"Output data folder: {output_data_dir}")
            
        except Exception as e:
            chunk.logger.error(f"Error preparing photometric stereo data: {e}")
            raise
        
        finally:
            chunk.logManager.end()