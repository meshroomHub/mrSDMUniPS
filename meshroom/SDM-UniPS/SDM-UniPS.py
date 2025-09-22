__version__ = "0.1"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL

class SDMUniPS(desc.Node):
    size = desc.DynamicNodeSize("inputSfmData")
    gpu = desc.Level.INTENSIVE
    parallelization = desc.Parallelization(blockSize=50)

    category = "Photometric Stereo"
    documentation = """
SDM-UniPS: Scalable, Detailed and Mask-free Universal Photometric Stereo Network (CVPR2023)

This node runs the SDM-UniPS neural network for photometric stereo reconstruction.
It processes preprocessed photometric stereo data to estimate surface normals and BRDF parameters.

The network can handle arbitrary lighting conditions without requiring calibrated lighting setup.
"""

    inputs = [
        desc.File(
            name="inputSfmData",
            label="Input SfMData",
            description="Preprocessed SfMData file from PreparePSImages node.",
            value="",
        ),
        desc.File(
            name="inputDataFolder",
            label="Data Folder",
            description="Preprocessed data folder from PreparePSImages node.",
            value="",
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
            name="outputSfmDataNormal",
            label="SfMData Normal",
            description="Output SfMData file containing the normal maps information.",
            value="{nodeCacheFolder}/normalMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="outputSfmDataAlbedo",
            label="SfMData Albedo",
            description="Output SfMData file containing the albedo information.",
            value="{nodeCacheFolder}/albedoMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="outputSfmDataRoughness",
            label="SfMData Roughness",
            description="Output SfMData file containing the roughness information.",
            value="{nodeCacheFolder}/roughnessMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="outputSfmDataMetallic",
            label="SfMData Metallic",
            description="Output SfMData file containing the metallic information.",
            value="{nodeCacheFolder}/metallicMaps.sfm",
            group="",  # remove from command line
        ),
        desc.File(
            name="normals",
            label="Normal Maps Camera",
            description="Generated normal maps in the camera coordinate system.",
            semantic="image",
            value="{nodeCacheFolder}/<POSE_ID>_normals.png",
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

    def createOutputSfmData(self, chunk):
        """
        Create SfMData files for the outputs, using pyalicevision library.
        """
        try:
            from pyalicevision import sfmData, sfmDataIO
            
            # Load input SfMData using pyalicevision
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputSfmData.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputSfmData.value}")

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
            
            # Create Normal SfMData
            normal_sfm_data = albedo_sfm_data
            views = normal_sfm_data.getViews()
            for view_id, view in views.items():
                pose_id = view.getPoseId()
                normal_path = f"{chunk.node.outputPath.value}/{pose_id}_normals.png"
                view.getImage().setImagePath(normal_path)
            
            if not sfmDataIO.save(normal_sfm_data,
                                    f"{chunk.node.outputPath.value}/normalMaps.sfm",
                                    sfmDataIO.ALL):
                chunk.logger.warning("Failed to save normal SfMData")
            else:
                chunk.logger.info(f"Normal SfMData saved to {chunk.node.outputPath.value}/normalMaps.sfm")

            # Create Albedo, Roughness and Metallic SfMData
            if chunk.node.target.value in ["brdf", "normal_and_brdf"]:
                
                # Save roughness and metallic maps as well
                for param in ["albedo", "roughness", "metallic"]:
                    param_sfm_data = albedo_sfm_data
                    views = param_sfm_data.getViews()
                    for view_id, view in views.items():
                        pose_id = view.getPoseId()
                        param_path = f"{chunk.node.outputPath.value}/{pose_id}_{param}.png"
                        view.getImage().setImagePath(param_path)
                    
                    if not sfmDataIO.save(param_sfm_data,
                                        f"{chunk.node.outputPath.value}/{param}Maps.sfm",
                                        sfmDataIO.ALL):
                        chunk.logger.warning(f"Failed to save {param} SfMData")
                    else:
                        chunk.logger.info(f"{param.capitalize()} SfMData saved to {chunk.node.outputPath.value}/{param}Maps.sfm")
            
        except Exception as e:
            chunk.logger.error(f"Error creating output SfMData files: {e}")
            raise

    def moveResultsToMeshroomOutput(self, chunk):
        """
        Move SDM-UniPS results from its output location to Meshroom expected locations.
        """
        try:
            import shutil
            from pathlib import Path
            from pyalicevision import sfmData, sfmDataIO

            # Load input SfMData to get pose information
            input_sfm_data = sfmData.SfMData()
            if not sfmDataIO.load(input_sfm_data, chunk.node.inputSfmData.value, sfmDataIO.ALL):
                raise RuntimeError(f"Failed to load input SfMData file: {chunk.node.inputSfmData.value}")

            # Get unique pose IDs
            pose_ids = set()
            views = input_sfm_data.getViews()
            for view_id, view in views.items():
                if view_id == view.getPoseId():  # Only representative views
                    pose_ids.add(view.getPoseId())

            chunk.logger.info(f"Moving results for {len(pose_ids)} poses from {chunk.node.tempFolder}")

            # Move results for each pose
            for pose_id in pose_ids:
                pose_results_dir = Path(chunk.node.tempFolder) / "results" / f"pose_{pose_id}{chunk.node.viewExt.value}"
                
                if not pose_results_dir.exists():
                    chunk.logger.warning(f"Results directory not found for pose {pose_id}: {pose_results_dir}")
                    continue

                chunk.logger.debug(f"Processing results for pose {pose_id}")

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
                            final_name = f"{pose_id}_normals.png"
                    elif "albedo" in filename or "basecolor" in filename:
                        final_name = f"{pose_id}_albedo.png"
                    elif "roughness" in filename:
                        final_name = f"{pose_id}_roughness.png"
                    elif "metallic" in filename:
                        final_name = f"{pose_id}_metallic.png"
                    else:
                        chunk.logger.debug(f"Skipping unknown result file: {result_file.name}")
                        continue

                    if final_name:
                        dst_path = Path(chunk.node.outputPath.value) / final_name
                        shutil.move(str(result_file), str(dst_path))
                        chunk.logger.debug(f"Moved {result_file.name} -> {final_name}")

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

            if not chunk.node.inputSfmData.value:
                raise RuntimeError("No input SfMData file provided")
            
            if not chunk.node.inputDataFolder.value:
                raise RuntimeError("No input data folder provided")
            
            # Use the preprocessed data folder directly
            data_dir = Path(chunk.node.inputDataFolder.value)
            
            if not data_dir.exists():
                raise RuntimeError(f"Input data folder does not exist: {data_dir}")
            
            # Temp output path for SDM-UniPS
            chunk.node.tempFolder = Path(chunk.node.outputPath.value) / "meshroom_sdm_unips"
            
            chunk.logger.info(f"Processing preprocessed data from: {data_dir}")

            chunk.logger.debug(f"Input SfMData: {chunk.node.inputSfmData.value}")
            chunk.logger.debug(f"Input Data Folder: {data_dir}")
            chunk.logger.debug(f"Temp Output Path: {chunk.node.tempFolder}")
            chunk.logger.debug(f"Checkpoint Path: {chunk.node.checkpoint.evalValue}")
            chunk.logger.debug(f"Target Output: {chunk.node.target.value}")
            chunk.logger.debug(f"Max Image Resolution: {chunk.node.maxImageRes.value}")
            chunk.logger.debug(f"Max Image Number: {chunk.node.maxImageNum.value}")
            chunk.logger.debug(f"View Extension: {chunk.node.viewExt.value}")
            chunk.logger.debug(f"Image Prefix: {chunk.node.imagePrefix.value}")
            chunk.logger.debug(f"Canonical Resolution: {chunk.node.canonicalResolution.value}")
            chunk.logger.debug(f"Pixel Samples: {chunk.node.pixelSamples.value}")
            chunk.logger.debug(f"Scalable Mode: {chunk.node.scalable.value}")
            chunk.logger.debug(f"Verbose Level: {chunk.node.verboseLevel.value}")

            # Initialize SDM-UniPS API
            sdm_api = SDMUniPS_API(
                checkpoint_path=chunk.node.checkpoint.evalValue,
                target=chunk.node.target.value,
                canonical_resolution=chunk.node.canonicalResolution.value,
                pixel_samples=chunk.node.pixelSamples.value,
                scalable=chunk.node.scalable.value,
                session_name=chunk.node.tempFolder,
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
                self.moveResultsToMeshroomOutput(chunk)
                
            else:
                raise RuntimeError("SDM-UniPS processing failed")

            # Post-process outputs to create SfMData files
            self.createOutputSfmData(chunk)

        finally:
            if 'sdm_api' in locals():
                del sdm_api
            torch.cuda.empty_cache()

            # Remove temporary SDM-UniPS output directory
            import shutil
            shutil.rmtree(Path("meshroom_sdm_unips"), ignore_errors=True)

            chunk.logManager.end()