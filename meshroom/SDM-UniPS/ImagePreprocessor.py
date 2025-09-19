__version__ = "0.1"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
import os
from pathlib import Path

class ImagePreprocessor(desc.Node):
    size = desc.DynamicNodeSize("inputPath")
    
    category = "Preprocessing"
    documentation = """
Image Preprocessor for Photometric Stereo

This node preprocesses images for photometric stereo processing by:
1. Ensuring all images are in landscape orientation (width > height)
2. Optionally cropping images based on a common bounding box estimated from masks
3. Updating camera intrinsics accordingly

This preprocessing is particularly useful for SDM-UniPS and other photometric stereo methods
that work better with consistent image orientations and cropping.
"""

    inputs = [
        desc.File(
            name="inputPath",
            label="Input SfMData",
            description="Input SfMData file containing images to preprocess.",
            value="",
        ),
        desc.File(
            name="maskPath",
            label="Mask Folder Path", 
            description="Path to a folder containing masks for bbox estimation, or to a single mask file.",
            value="",
        ),
        desc.BoolParam(
            name="enableCropping",
            label="Enable Cropping",
            description="Enable cropping based on mask bounding box estimation.",
            value=True,
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
            label="Output SfMData",
            description="Output SfMData file with preprocessed image information.",
            value="{nodeCacheFolder}/sfmData.sfm",
        ),
        desc.File(
            name="outputImagesFolder",
            label="Output Images Folder",
            description="Folder containing the preprocessed images.",
            value="{nodeCacheFolder}/images",
        ),
    ]

    def processChunk(self, chunk):
        """
        Process the image preprocessing.
        """
        try:
            from .utils import preprocess_images_and_sfmdata
            
            chunk.logManager.start("Image Preprocessing")
            
            if not chunk.node.inputPath.value:
                raise RuntimeError("No input SfMData file provided")
            
            # Prepare mask paths if provided
            mask_paths = []
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
                else:
                    chunk.logger.warning(f"Mask path does not exist: {chunk.node.maskPath.value}")
            
            # Determine target crop size
            target_crop_size = None
            if (chunk.node.enableCropping.value and 
                chunk.node.targetCropWidth.value > 0 and 
                chunk.node.targetCropHeight.value > 0):
                target_crop_size = (chunk.node.targetCropWidth.value, chunk.node.targetCropHeight.value)
            
            # Create output directories
            output_images_dir = Path(chunk.node.outputImagesFolder.value)
            output_images_dir.mkdir(parents=True, exist_ok=True)
            
            # Process images and SfMData
            chunk.logger.info("Starting image preprocessing...")
            result = preprocess_images_and_sfmdata(
                input_sfm_path=chunk.node.inputPath.value,
                output_sfm_path=chunk.node.outputPath.value,
                output_images_dir=str(output_images_dir),
                mask_paths=[str(p) for p in mask_paths] if mask_paths else None,
                enable_cropping=chunk.node.enableCropping.value,
                target_crop_size=target_crop_size,
                logger=chunk.logger
            )
            
            if result["success"]:
                chunk.logger.info(f"Preprocessing completed successfully")
                chunk.logger.info(f"Processed {result['processed_count']} images")
                if result.get('common_bbox'):
                    chunk.logger.info(f"Applied common bbox: {result['common_bbox']}")
            else:
                raise RuntimeError(f"Preprocessing failed: {result.get('error', 'Unknown error')}")
                
            chunk.logManager.end("Image Preprocessing completed successfully")
            
        except Exception as e:
            chunk.logger.error(f"Error in image preprocessing: {e}")
            raise