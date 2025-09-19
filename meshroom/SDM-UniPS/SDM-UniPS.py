__version__ = "0.1"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL

class SDMUniPS(desc.Node):
    size = desc.DynamicNodeSize("inputPath")
    gpu = desc.Level.INTENSIVE
    parallelization = desc.Parallelization(blockSize=50)

    category = "Photometric Stereo"
    documentation = """
SDM-UniPS: Scalable, Detailed and Mask-free Universal Photometric Stereo Network (CVPR2023)

This node runs the SDM-UniPS neural network for photometric stereo reconstruction.
It processes multiple images taken under different lighting conditions to estimate surface normals and BRDF parameters.

The network can handle arbitrary lighting conditions without requiring calibrated lighting setup.
"""

    inputs = [
        desc.File(
            name="inputPath",
            label="SfMData",
            description="Input SfMData file.",
            value="",
        ),
        desc.File(
            name="maskPath",
            label="Mask Folder Path", 
            description="Path to a folder containing masks or to a mask directly.",
            value="",
        ),
        desc.BoolParam(
            name="enableCropping",
            label="Enable Cropping",
            description="Enable cropping based on mask bounding box estimation. If disabled, only landscape orientation will be applied.",
            value=False,
        ),
        desc.ChoiceParam(
            name="target",
            label="Target Output",
            description="What to estimate: normal maps only, BRDF only, or both.",
            values=["normal", "brdf", "normal_and_brdf"],
            value="normal_and_brdf",
        ),
        desc.File(
            name="checkpoint",
            label="Checkpoint Path",
            description="Path to the model checkpoint file.",
            value="${SDM_UNIPS_CHECKPOINT_PATH}",
        ),
        desc.IntParam(
            name="maxImageRes",
            label="Max Image Resolution",
            description="Maximum image resolution for processing.",
            value=4096,
            range=(512, 8192, 1),
            advanced=True,
        ),
        desc.IntParam(
            name="maxImageNum",
            label="Max Image Number",
            description="Maximum number of images to process per pose.",
            value=10,
            range=(3, 50, 1),
            advanced=True,
        ),
        desc.StringParam(
            name="viewExt",
            label="View Extension",
            description="Extension of the view folders (e.g., .data, .png). See SDM-UniPS documentation for details.",
            value=".data",
            advanced=True,
        ),
        desc.StringParam(
            name="imagePrefix",
            label="Image Prefix",
            description="Prefix pattern for test images (e.g., L* for images starting with L). See SDM-UniPS documentation for details.",
            value="L*",
            advanced=True,
        ),
        desc.IntParam(
            name="canonicalResolution",
            label="Canonical Resolution",
            description="Canonical resolution. See SDM-UniPS documentation for details.",
            value=256,
            range=(64, 1024, 1),
            advanced=True,
        ),
        desc.IntParam(
            name="pixelSamples",
            label="Pixel Samples",
            description="Number of pixel samples. See SDM-UniPS documentation for details.",
            value=10000,
            range=(1000, 50000, 1000),
            advanced=True,
        ),
        desc.BoolParam(
            name="scalable",
            label="Scalable Mode",
            description="Enable scalable mode for large images.",
            value=False,
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
            name="outputPath",
            label="Output Folder",
            description="Path to the output folder.",
            value="{nodeCacheFolder}",
        ),
        desc.File(
            name="outputSfmDataAlbedo",
            label="SfMData Albedo",
            description="Output SfMData file containing the albedo information.",
            value="{nodeCacheFolder}/albedoMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="outputSfmDataNormal",
            label="SfMData Normal",
            description="Output SfMData file containing the normal maps information.",
            value="{nodeCacheFolder}/normalMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="normals",
            label="Normal Maps Camera",
            description="Generated normal maps in the camera coordinate system.",
            semantic="image",
            value="{nodeCacheFolder}/<POSE_ID>_normals.exr",
            group="",
        ),
        desc.File(
            name="albedo",
            label="Albedo Maps",
            description="Generated albedo maps.",
            semantic="image",
            value="{nodeCacheFolder}/<POSE_ID>_albedo.png",
            group="",  # do not export on the command line
        ),
        desc.File(
            name="roughness",
            label="Roughness Maps",
            description="Generated roughness maps (BRDF parameter).",
            semantic="image",
            value="{nodeCacheFolder}/<POSE_ID>_roughness.png",
            group="",  # do not export on the command line
        ),
        desc.File(
            name="metallic",
            label="Metallic Maps",
            description="Generated metallic maps (BRDF parameter).",
            semantic="image",
            value="{nodeCacheFolder}/<POSE_ID>_metallic.png",
            group="",  # do not export on the command line
        ),
    ]

    def prepareSDMUniPSData(self, chunk):
        """
        Prepare data for SDM-UniPS processing.
        This function extracts images and masks from the input SfMData and organizes them for SDM-UniPS.
        """
        try:
            import shutil
            import cv2
            import numpy as np
            import os
            from pathlib import Path
            from pyalicevision import sfmData, sfmDataIO
            from utils.utils import ensure_landscape_orientation, estimate_common_bbox_from_masks

            # Load input SfMData
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputPath.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputPath.value}")

            # First, collect mask paths for preprocessing (including alpha channels) - only if cropping is enabled
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
                                temp_mask_path = Path(chunk.node.outputPath.value) / f"temp_alpha_mask_{pose_id}.png"
                                temp_mask_path.parent.mkdir(parents=True, exist_ok=True)
                                cv2.imwrite(str(temp_mask_path), alpha_mask)
                                alpha_mask_paths.append(temp_mask_path)
                                chunk.logger.debug(f"Extracted alpha channel from representative image for pose {pose_id}")
                
                # Combine external masks and alpha channel masks
                all_mask_paths = mask_paths + alpha_mask_paths
                
                if all_mask_paths:
                    chunk.logger.info(f"Collected {len(mask_paths)} external masks and {len(alpha_mask_paths)} alpha channel masks for preprocessing")
                    
                    # Estimate common bbox if cropping is enabled and masks are provided
                    chunk.logger.info(f"Estimating common bbox from {len(all_mask_paths)} masks")
                    common_bbox = estimate_common_bbox_from_masks(all_mask_paths, target_size=None)
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
                chunk.logger.info("Cropping disabled - only landscape orientation will be applied")

            # Get views per pose ID
            views_per_pose_id = {}
            views = input_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                if pose_id not in views_per_pose_id:
                    views_per_pose_id[pose_id] = []
                views_per_pose_id[pose_id].append(view_id)

            # Create data directories for SDM-UniPS and process images directly
            data_dir = Path(chunk.node.outputPath.value) / "sdm_unips_data"
            data_dir.mkdir(parents=True, exist_ok=True)

            # Create updated SfMData with new image paths
            updated_sfm_data = input_sfm_data
            processed_count = 0

            # Process each pose separately
            for pose_id, view_ids in views_per_pose_id.items():
                chunk.logger.info(f"Preparing data for Pose Id: {pose_id}")
                
                # Create pose directory with SDM-UniPS expected naming
                pose_dir = data_dir / f"pose_{pose_id}{chunk.node.viewExt.value}"
                pose_dir.mkdir(parents=True, exist_ok=True)

                # Get image list for this pose
                image_list = []
                for view_id in view_ids:
                    view = input_sfm_data.getView(view_id)
                    image_path = view.getImage().getImagePath()
                    chunk.logger.info(f" - {image_path}")
                    image_list.append((view_id, image_path))

                if len(image_list) < 1:
                    chunk.logger.warning(f"Empty image list for pose {pose_id}, skipping.")
                    continue

                # Process images directly with SDM-UniPS naming and handle alpha channel
                prefix = chunk.node.imagePrefix.value.replace("*", "")  # Remove wildcard
                alpha_mask = None
                alpha_mask_found = False
                
                for i, (view_id, image_path) in enumerate(image_list):
                    if not os.path.isfile(image_path):
                        chunk.logger.warning(f"Image file not found: {image_path}")
                        continue
                    
                    src_path = Path(image_path)
                    # Create filename with L prefix and zero-padded index
                    dst_filename = f"{prefix}{i:03d}{src_path.suffix}"
                    dst_path = pose_dir / dst_filename
                    
                    # Load and preprocess image
                    img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
                    if img is None:
                        chunk.logger.warning(f"Could not read image: {image_path}")
                        continue
                    
                    original_size = (img.shape[1], img.shape[0])  # (width, height)
                    
                    # Handle alpha channel extraction only for representative images (viewId == poseId)
                    if view_id == pose_id and len(img.shape) == 3 and img.shape[2] == 4:
                        chunk.logger.debug(f"Alpha channel detected in {src_path.name}")
                        
                        # Extract alpha channel as mask (first image sets the mask)
                        if not alpha_mask_found:
                            alpha_mask = img[:, :, 3]  # Extract alpha channel
                            alpha_mask_found = True
                            chunk.logger.debug(f"Using alpha channel from {src_path.name} as mask for pose {pose_id}")
                        
                        # Remove alpha channel and keep only RGB
                        img = img[:, :, :3]  # Keep only RGB channels
                    
                    # Apply preprocessing: ensure landscape orientation
                    processed_img, rotation_applied = ensure_landscape_orientation(img)
                    
                    if rotation_applied > 0:
                        chunk.logger.debug(f"Rotated image {src_path.name} by {rotation_applied} degrees")
                    
                    # Apply cropping if enabled and bbox is available
                    if chunk.node.enableCropping.value and common_bbox:
                        crop_x, crop_y, crop_w, crop_h = common_bbox
                        processed_img = processed_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                        chunk.logger.debug(f"Cropped image {src_path.name} to {crop_w}x{crop_h}")
                    
                    # Save processed image directly to SDM-UniPS location
                    cv2.imwrite(str(dst_path), processed_img)
                    chunk.logger.debug(f"Processed and saved {src_path.name} -> {dst_filename}")
                    
                    # Update SfMData with new image path and dimensions
                    view = updated_sfm_data.getView(view_id)
                    view.getImage().setImagePath(str(dst_path))
                    new_height, new_width = processed_img.shape[:2]
                    view.getImage().setWidth(new_width)
                    view.getImage().setHeight(new_height)
                    
                    # Note: Intrinsics are not updated since we couldn't find a reliable way to do it
                    # The user should be aware that intrinsics might not match the processed images
                    if view_id == pose_id and (rotation_applied > 0 or (chunk.node.enableCropping.value and common_bbox)):
                        chunk.logger.warning(f"Image preprocessing applied for pose {pose_id} but intrinsics were not updated. "
                                           f"Rotation: {rotation_applied}°, Cropping: {'Yes' if chunk.node.enableCropping.value and common_bbox else 'No'}")
                    
                    processed_count += 1

                # Handle mask: alpha channel takes priority, then external mask
                mask_copied = False
                
                # First, process and save alpha channel mask if found
                if alpha_mask_found and alpha_mask is not None:
                    # Apply same preprocessing to alpha mask
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
                                # Apply the same preprocessing to the mask
                                mask_img = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)
                                if mask_img is not None:
                                    # Apply same transformations as images
                                    processed_mask, _ = ensure_landscape_orientation(mask_img)
                                    if chunk.node.enableCropping.value and common_bbox:
                                        crop_x, crop_y, crop_w, crop_h = common_bbox
                                        processed_mask = processed_mask[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                                    
                                    cv2.imwrite(str(pose_dir / "mask.png"), processed_mask)
                                    chunk.logger.debug(f"Copied and processed external mask: {pattern}")
                                    mask_copied = True
                                    break
                        
                        if not mask_copied:
                            chunk.logger.debug(f"No external mask found for pose {pose_id} in {chunk.node.maskPath.value}")
                            
                    elif os.path.isfile(chunk.node.maskPath.value):
                        # Single mask file for all poses - apply same preprocessing
                        mask_img = cv2.imread(chunk.node.maskPath.value, cv2.IMREAD_GRAYSCALE)
                        if mask_img is not None:
                            processed_mask, _ = ensure_landscape_orientation(mask_img)
                            if chunk.node.enableCropping.value and common_bbox:
                                crop_x, crop_y, crop_w, crop_h = common_bbox
                                processed_mask = processed_mask[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
                            
                            cv2.imwrite(str(pose_dir / "mask.png"), processed_mask)
                            chunk.logger.debug(f"Copied and processed global external mask for pose {pose_id}")
                            mask_copied = True
                    else:
                        chunk.logger.debug(f"External mask path is neither a directory nor a file: {chunk.node.maskPath.value}")

                if not mask_copied:
                    chunk.logger.debug(f"No mask used for pose {pose_id} (SDM-UniPS is mask-free)")

                chunk.logger.info(f"Prepared {len(image_list)} images for pose {pose_id} in {pose_dir}")

            # Save updated SfMData with new image paths and updated dimensions (but not intrinsics)
            updated_sfm_path = Path(chunk.node.outputPath.value) / "preprocessed_sfmData.sfm"
            if not sfmDataIO.save(updated_sfm_data, str(updated_sfm_path), sfmDataIO.ALL):
                chunk.logger.warning(f"Failed to save updated SfMData to: {updated_sfm_path}")
            else:
                chunk.logger.debug(f"Updated SfMData saved to: {updated_sfm_path}")

            chunk.logger.info(f"SDM-UniPS data preparation completed in {data_dir}")
            chunk.logger.info(f"Processed {processed_count} images total")
            
            if processed_count > 0:
                chunk.logger.info("Note: Images were processed for landscape orientation and/or cropping, but camera intrinsics were not updated.")
                chunk.logger.info("The intrinsics in the SfMData may not match the processed images.")
            
            # Store the data directory path for use in processChunk
            chunk.node._sdm_unips_data_dir = str(data_dir)
            
        except Exception as e:
            chunk.logger.error(f"Error preparing SDM-UniPS data: {e}")
            raise

    def createOutputSfmData(self, chunk, views_per_pose_id):
        """
        Create SfMData files for the outputs, using pyalicevision library.
        """
        try:
            import os
            from pyalicevision import sfmData, sfmDataIO
            
            # Load input SfMData using pyalicevision
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputPath.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputPath.value}")

            # Create Albedo SfMData (copy of input)
            albedo_sfm_data = input_sfm_data
            view_ids_to_remove = set()
            
            # Filter views: keep only pose representative views (viewId == poseId)
            views = albedo_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                
                if view_id == pose_id:
                    # Set albedo image path for this pose
                    albedo_path = f"{chunk.node.outputPath.value}/{pose_id}_albedo.png"
                    view.getImage().setImagePath(albedo_path)
                else:
                    view_ids_to_remove.add(view_id)
            
            # Remove non-representative views
            for view_id in view_ids_to_remove:
                albedo_sfm_data.getViews().erase(view_id)
            
            # Save albedo SfMData
            if not sfmDataIO.save(albedo_sfm_data, 
                                 f"{chunk.node.outputPath.value}/albedoMaps.sfm",
                                 sfmDataIO.ESfMData(sfmDataIO.VIEWS | sfmDataIO.INTRINSICS | sfmDataIO.EXTRINSICS)):
                chunk.logger.warning("Failed to save albedo SfMData")
            else:
                chunk.logger.info(f"Albedo SfMData saved to {chunk.node.outputPath.value}/albedoMaps.sfm")
            
            # Create Normal SfMData (copy of albedo data)
            normal_sfm_data = albedo_sfm_data
            views = normal_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                normal_path = f"{chunk.node.outputPath.value}/{pose_id}_normals_w.exr"
                view.getImage().setImagePath(normal_path)
            
            if not sfmDataIO.save(normal_sfm_data,
                                 f"{chunk.node.outputPath.value}/normalMaps.sfm",
                                 sfmDataIO.ESfMData(sfmDataIO.VIEWS | sfmDataIO.INTRINSICS | sfmDataIO.EXTRINSICS)):
                chunk.logger.warning("Failed to save normal SfMData")
            else:
                chunk.logger.info(f"Normal SfMData saved to {chunk.node.outputPath.value}/normalMaps.sfm")
            
            # Create Normal PNG SfMData (copy of albedo data)
            normal_png_sfm_data = albedo_sfm_data
            views = normal_png_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                normal_png_path = f"{chunk.node.outputPath.value}/{pose_id}_normals_w.png"
                view.getImage().setImagePath(normal_png_path)
            
            if not sfmDataIO.save(normal_png_sfm_data,
                                 f"{chunk.node.outputPath.value}/normalMapsPNG.sfm",
                                 sfmDataIO.ESfMData(sfmDataIO.VIEWS | sfmDataIO.INTRINSICS | sfmDataIO.EXTRINSICS)):
                chunk.logger.warning("Failed to save normal PNG SfMData")
            else:
                chunk.logger.info(f"Normal PNG SfMData saved to {chunk.node.outputPath.value}/normalMapsPNG.sfm")
            
        except Exception as e:
            chunk.logger.error(f"Error creating output SfMData files: {e}")
            raise

    def moveResultsToMeshroomOutput(self, chunk, sdm_output_path):
        """
        Move SDM-UniPS results from its output location to Meshroom expected locations.
        """
        try:
            import shutil
            import os
            from pathlib import Path
            from pyalicevision import sfmData, sfmDataIO

            # Load input SfMData to get pose information
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputPath.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputPath.value}")

            # Get unique pose IDs
            pose_ids = set()
            views = input_sfm_data.getViews()
            for view_id, view in views.items():
                if view_id == view.getPoseId():  # Only representative views
                    pose_ids.add(view.getPoseId())

            chunk.logger.info(f"Moving results for {len(pose_ids)} poses from {sdm_output_path}")

            # Move results for each pose
            for pose_id in pose_ids:
                pose_results_dir = Path(sdm_output_path) / "results" / f"pose_{pose_id}{chunk.node.viewExt.value}"
                
                if not pose_results_dir.exists():
                    chunk.logger.warning(f"Results directory not found for pose {pose_id}: {pose_results_dir}")
                    continue

                chunk.logger.info(f"Processing results for pose {pose_id}")

                # Move each type of result file
                for result_file in pose_results_dir.glob("*"):
                    if not result_file.is_file():
                        continue

                    filename = result_file.name.lower()
                    final_name = None

                    # Determine output filename based on content
                    if "normal" in filename:
                        if result_file.suffix == ".exr":
                            final_name = f"{pose_id}_normals.exr"
                        else:
                            final_name = f"{pose_id}_normals_w.png"
                    elif "albedo" in filename or "basecolor" in filename:
                        final_name = f"{pose_id}_albedo.png"
                    elif "roughness" in filename:
                        final_name = f"{pose_id}_roughness.png"
                    elif "metallic" in filename:
                        final_name = f"{pose_id}_metallic.png"
                    else:
                        chunk.logger.info(f"Skipping unknown result file: {result_file.name}")
                        continue

                    if final_name:
                        dst_path = Path(chunk.node.outputPath.value) / final_name
                        shutil.move(str(result_file), str(dst_path))
                        chunk.logger.info(f"Moved {result_file.name} -> {final_name}")

        except Exception as e:
            chunk.logger.error(f"Error moving SDM-UniPS results: {e}")
            raise


    def processChunk(self, chunk):
        """
        Process the SDM-UniPS photometric stereo reconstruction.
        """
        from pathlib import Path
        from sdm_unips.api import SDMUniPS_API
        import torch

        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            if not chunk.node.inputPath.value:
                raise RuntimeError("No input SfMData file provided")
                        
            # Prepare data from input SfMData and masks
            # self.prepareSDMUniPSData(chunk)
            chunk.node._sdm_unips_data_dir = Path(chunk.node.outputPath.value) / "sdm_unips_data"

            # Get the prepared data directory
            data_dir = chunk.node._sdm_unips_data_dir
            chunk.logger.info(f"Processing data from: {data_dir}")

            # Add this debugging code before sdm_api.process_dataset()
            chunk.logger.debug("=== DEBUG: Parameter Comparison ===")
            chunk.logger.debug(f"test_dir: {data_dir}")
            chunk.logger.debug(f"max_image_res: {chunk.node.maxImageRes.value}")
            chunk.logger.debug(f"max_image_num: {chunk.node.maxImageNum.value}")
            chunk.logger.debug(f"test_ext: {chunk.node.viewExt.value}")
            chunk.logger.debug(f"test_prefix: {chunk.node.imagePrefix.value}")
            chunk.logger.debug(f"target: {chunk.node.target.value}")
            chunk.logger.debug(f"canonical_resolution: {chunk.node.canonicalResolution.value}")
            chunk.logger.debug(f"pixel_samples: {chunk.node.pixelSamples.value}")
            chunk.logger.debug(f"scalable: {chunk.node.scalable.value}")
            chunk.logger.debug("=====================================")

            # Initialize SDM-UniPS API
            sdm_api = SDMUniPS_API(
                checkpoint_path=chunk.node.checkpoint.value,
                target=chunk.node.target.value,
                canonical_resolution=chunk.node.canonicalResolution.value,
                pixel_samples=chunk.node.pixelSamples.value,
                scalable=chunk.node.scalable.value,
                session_name="meshroom_sdm_unips"
            )

            # Process the dataset
            chunk.logger.info("Starting SDM-UniPS processing...")
            result = sdm_api.process_dataset(
                test_dir=data_dir,
                max_image_res=chunk.node.maxImageRes.value,
                max_image_num=chunk.node.maxImageNum.value,
                test_ext=chunk.node.viewExt.value,
                test_prefix=chunk.node.imagePrefix.value,
                mask_margin=8  # Default mask margin
            )

            if result['success']:
                chunk.logger.info(f"SDM-UniPS processing completed successfully in {result['elapsed_time']:.2f} seconds")
                chunk.logger.info(f"Processed {result['num_objects']} objects")
                
                # Move results from SDM-UniPS output location to Meshroom expected locations
                self.moveResultsToMeshroomOutput(chunk, result['output_path'])
                
            else:
                raise RuntimeError("SDM-UniPS processing failed")

            # Post-process outputs to create SfMData files similar to PhotometricStereo
            self.createOutputSfmData(chunk, None)  # views_per_pose_id not needed here

        finally:
            del processor
            torch.cuda.empty_cache()
            chunk.logManager.end()