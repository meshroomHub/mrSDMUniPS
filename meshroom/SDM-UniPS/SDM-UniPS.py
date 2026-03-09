__version__ = "1.0"

import json
import os
from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL


class SDMUniPS(desc.Node):
    """
    Multi-view photometric stereo estimation using SDM-UniPS.

    Reads an SfMData JSON with multi-lighting views grouped by poseId,
    runs normal and/or BRDF estimation per pose, and outputs maps with
    output SfMData files and a JSON referencing all results.
    """

    category = "Photometric Stereo"
    gpu = desc.Level.INTENSIVE
    size = desc.DynamicNodeSize("inputSfm")

    documentation = """
    Estimate surface normals and BRDF parameters from multi-lighting
    images using SDM-UniPS (CVPR2023).

    **Inputs:**
    - SfMData JSON with views grouped by poseId (multi-lighting)
    - Optional mask folder (masks named by poseId or viewId)

    **Processing:**
    - Images are loaded and preprocessed internally
    - Normal maps and/or BRDF maps are estimated per pose

    **Outputs:**
    - Normal map PNGs per pose
    - BRDF maps (albedo, roughness, metallic) per pose
    - Output SfMData files referencing results
    - JSON file mapping poseIds to normal map paths
    """

    inputs = [
        desc.File(
            name="inputSfm",
            label="Input SfMData",
            description="SfMData JSON file with multi-lighting views "
                        "grouped by poseId.",
            value="",
        ),
        desc.File(
            name="maskFolder",
            label="Mask Folder",
            description="Folder with mask PNGs named by poseId or viewId "
                        "(e.g. '12345.png'). Optional.",
            value="",
        ),
        desc.IntParam(
            name="downscale",
            label="Downscale Factor",
            description="Integer downscale factor for input images "
                        "(1 = original, 2 = half, 4 = quarter).",
            value=1,
            range=(1, 8, 1),
        ),
        desc.IntParam(
            name="nbImages",
            label="Number of Images",
            description="Maximum number of lighting images per pose to use.",
            value=10,
            range=(3, 50, 1),
        ),
        desc.ChoiceParam(
            name="target",
            label="Target Output",
            description="What to estimate: normal maps only, BRDF only, "
                        "or both.",
            values=["normal", "brdf", "normal_and_brdf"],
            value="normal_and_brdf",
        ),
        desc.BoolParam(
            name="useGpu",
            label="Use GPU",
            description="Use GPU for inference.",
            value=True,
            invalidate=False,
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
            name="canonicalResolution",
            label="Canonical Resolution",
            description="Canonical resolution for the network. "
                        "See SDM-UniPS documentation for details.",
            value=256,
            range=(64, 1024, 1),
            advanced=True,
        ),
        desc.IntParam(
            name="pixelSamples",
            label="Pixel Samples",
            description="Number of pixel samples for processing. "
                        "See SDM-UniPS documentation for details.",
            value=10000,
            range=(1000, 50000, 1),
            advanced=True,
        ),
        desc.BoolParam(
            name="scalable",
            label="Scalable Mode",
            description="Enable scalable mode for large images.",
            value=False,
            advanced=True,
        ),
        desc.File(
            name="sdmUniPsPath",
            label="SDM-UniPS Path",
            description="Path to SDM-UniPS code directory. "
                        "Set via config.json key SDM_UNIPS_PATH.",
            value="${SDM_UNIPS_PATH}",
            advanced=True,
        ),
        desc.File(
            name="checkpoint",
            label="Checkpoint Path",
            description="Path to the model checkpoint directory. "
                        "Set via config.json key SDM_UNIPS_CHECKPOINT_PATH.",
            value="${SDM_UNIPS_CHECKPOINT_PATH}",
            advanced=True,
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level for logging.",
            values=VERBOSE_LEVEL,
            value="info",
            exclusive=True,
        ),
    ]

    outputs = [
        desc.File(
            name="outputFolder",
            label="Output Folder",
            description="Folder containing output maps.",
            value="{nodeCacheFolder}",
        ),
        desc.File(
            name="outputSfmDataNormal",
            label="SfMData Normal",
            description="Output SfMData file referencing normal maps.",
            value="{nodeCacheFolder}/normalMaps.sfm",
            group="",
        ),
        desc.File(
            name="outputSfmDataAlbedo",
            label="SfMData Albedo",
            description="Output SfMData file referencing albedo maps.",
            value="{nodeCacheFolder}/albedoMaps.sfm",
            group="",
        ),
        desc.File(
            name="outputSfmDataRoughness",
            label="SfMData Roughness",
            description="Output SfMData file referencing roughness maps.",
            value="{nodeCacheFolder}/roughnessMaps.sfm",
            group="",
        ),
        desc.File(
            name="outputSfmDataMetallic",
            label="SfMData Metallic",
            description="Output SfMData file referencing metallic maps.",
            value="{nodeCacheFolder}/metallicMaps.sfm",
            group="",
        ),
        desc.File(
            name="normalMaps",
            label="Normal Maps",
            description="Normal map images.",
            semantic="image",
            value="{nodeCacheFolder}/<VIEW_ID>_normals.png",
            group="",
        ),
        desc.File(
            name="albedoMaps",
            label="Albedo Maps",
            description="Albedo map images.",
            semantic="image",
            value="{nodeCacheFolder}/<VIEW_ID>_albedo.png",
            group="",
        ),
        desc.File(
            name="roughnessMaps",
            label="Roughness Maps",
            description="Roughness map images.",
            semantic="image",
            value="{nodeCacheFolder}/<VIEW_ID>_roughness.png",
            group="",
        ),
        desc.File(
            name="metallicMaps",
            label="Metallic Maps",
            description="Metallic map images.",
            semantic="image",
            value="{nodeCacheFolder}/<VIEW_ID>_metallic.png",
            group="",
        ),
        desc.File(
            name="outputMaskFolder",
            label="Mask Folder",
            description="Folder with masks extracted from alpha channels.",
            value="{nodeCacheFolder}/masks",
            group="",
        ),
    ]

    @staticmethod
    def _scale_intrinsics(sfm, downscale):
        """Scale intrinsics and view dimensions to match downscaled images."""
        if downscale <= 1:
            return
        f = float(downscale)
        for intr in sfm.get("intrinsics", []):
            for key in ("width", "height"):
                if key in intr:
                    intr[key] = str(int(int(float(str(intr[key]))) / f))
            if "principalPoint" in intr:
                pp = intr["principalPoint"]
                intr["principalPoint"] = [
                    str(float(str(pp[0])) / f),
                    str(float(str(pp[1])) / f),
                ]
            if "pxFocalLength" in intr:
                pfl = intr["pxFocalLength"]
                if isinstance(pfl, list):
                    intr["pxFocalLength"] = [pfl[0] / f, pfl[1] / f]
                else:
                    intr["pxFocalLength"] = float(pfl) / f
        for view in sfm.get("views", []):
            for key in ("width", "height"):
                if key in view:
                    view[key] = str(int(int(float(str(view[key]))) / f))

    def _create_output_sfm(self, sfm_data, output_folder,
                           map_type, suffix, logger, downscale=1):
        """Create an output SfMData JSON that references generated map files.

        Keeps one representative view per poseId (viewId == poseId),
        replaces image paths, and scales intrinsics for downscale.
        """
        import copy
        sfm = copy.deepcopy(sfm_data)

        views = sfm.get("views", [])

        representative_views = []
        for view in views:
            view_id = str(view.get("viewId", ""))
            pose_id = str(view.get("poseId", ""))
            if view_id == pose_id:
                map_path = os.path.join(output_folder,
                                        "{}{}".format(pose_id, suffix))
                view["path"] = map_path
                representative_views.append(view)

        sfm["views"] = representative_views
        self._scale_intrinsics(sfm, downscale)

        output_path = os.path.join(output_folder,
                                   "{}.sfm".format(map_type))
        with open(output_path, "w") as f:
            json.dump(sfm, f, indent=4)

        logger.info("Saved {} to {}".format(map_type, output_path))
        return output_path

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            # Validate inputs
            input_sfm = chunk.node.inputSfm.value
            if not input_sfm:
                raise RuntimeError("inputSfm is required but empty.")
            if not os.path.exists(input_sfm):
                raise RuntimeError(
                    "Input SfM file not found: {}".format(input_sfm))

            mask_folder = chunk.node.maskFolder.value or ""
            if mask_folder and not os.path.isdir(mask_folder):
                chunk.logger.warning(
                    "Mask folder not found, continuing without "
                    "masks: {}".format(mask_folder))
                mask_folder = ""

            # Resolve SDM-UniPS path
            sdm_path = chunk.node.sdmUniPsPath.evalValue
            if not sdm_path or not os.path.isdir(sdm_path):
                raise RuntimeError(
                    "SDM_UNIPS_PATH is empty or not a valid directory. "
                    "Set it in config.json. Got: '{}'".format(sdm_path))

            # Import SDM-UniPS modules (pip install or sys.path fallback)
            import sys
            try:
                from inference_sfm import (
                    load_sfm, group_views_by_pose,
                    find_mask_for_pose, load_images_for_pose,
                    preprocess_for_pose, load_model,
                    infer_pose,
                    save_normal_16bit, save_color_16bit,
                    save_gray_16bit,
                )
                import sdm_unips.modules.model.model
                import sdm_unips.modules.model.model_utils
                import sdm_unips.modules.model.decompose_tensors
            except ImportError:
                original_path = sys.path[:]
                sys.path.insert(0, sdm_path)
                try:
                    from inference_sfm import (
                        load_sfm, group_views_by_pose,
                        find_mask_for_pose, load_images_for_pose,
                        preprocess_for_pose, load_model,
                        infer_pose,
                        save_normal_16bit, save_color_16bit,
                        save_gray_16bit,
                    )
                    import sdm_unips.modules.model.model
                    import sdm_unips.modules.model.model_utils
                    import sdm_unips.modules.model.decompose_tensors
                except ImportError as e:
                    raise RuntimeError(
                        "Failed to import from SDM-UniPS at {}: {}".format(
                            sdm_path, e))
                finally:
                    sys.path[:] = original_path

            # Device selection
            import torch
            import numpy as np
            use_gpu = chunk.node.useGpu.value
            use_cuda = use_gpu and torch.cuda.is_available()
            if use_gpu and not use_cuda:
                chunk.logger.warning(
                    "CUDA not available, falling back to CPU")
            device = torch.device(
                "cuda" if use_cuda else "cpu")

            # Output folder
            output_folder = chunk.node.outputFolder.value
            os.makedirs(output_folder, exist_ok=True)

            # Resolve checkpoint path
            checkpoint_path = chunk.node.checkpoint.evalValue
            if not checkpoint_path or not os.path.isdir(checkpoint_path):
                # Fallback: look in plugin directory
                plugin_ckpt = os.path.join(
                    os.path.dirname(__file__), '..', '..', 'checkpoint')
                plugin_ckpt = os.path.abspath(plugin_ckpt)
                if os.path.isdir(plugin_ckpt):
                    checkpoint_path = plugin_ckpt
                    chunk.logger.info(
                        "Using plugin checkpoint: {}".format(checkpoint_path))
                else:
                    raise RuntimeError(
                        "Checkpoint directory not found. "
                        "Run download_weights.sh or set "
                        "SDM_UNIPS_CHECKPOINT_PATH in config.json.")

            # Parameters
            target = chunk.node.target.value
            downscale = chunk.node.downscale.value
            nb_img = chunk.node.nbImages.value
            max_image_res = chunk.node.maxImageRes.value
            canonical_res = chunk.node.canonicalResolution.value
            pixel_samples = chunk.node.pixelSamples.value
            scalable = chunk.node.scalable.value
            mask_output_folder = chunk.node.outputMaskFolder.value

            chunk.logger.info("Starting SDM-UniPS inference...")
            chunk.logger.info("  Input SfM: {}".format(input_sfm))
            chunk.logger.info("  Masks: {}".format(
                mask_folder or "(none)"))
            chunk.logger.info("  Downscale: {}".format(downscale))
            chunk.logger.info("  Target: {}".format(target))
            chunk.logger.info("  GPU: {}".format(use_cuda))
            chunk.logger.info("  Checkpoint: {}".format(
                checkpoint_path or "(default)"))

            # Load SfM data
            sfm_data = load_sfm(input_sfm)
            pose_groups = group_views_by_pose(sfm_data)
            chunk.logger.info("Loaded {} views, {} poses".format(
                len(sfm_data.get("views", [])), len(pose_groups)))

            # Load model
            chunk.logger.info("Loading SDM-UniPS model on {}...".format(
                device))
            net_nml, net_brdf = load_model(
                checkpoint_path, target, pixel_samples, device)
            chunk.logger.info("Model loaded")

            # Process each pose
            import time
            results = []
            total_start = time.time()
            num_poses = len(pose_groups)

            for i, (pose_id, views) in enumerate(
                    pose_groups.items()):
                chunk.logger.info(
                    "=== Pose {} ({}/{}, {} views) ===".format(
                        pose_id, i + 1, num_poses, len(views)))

                try:
                    # Load images
                    images = load_images_for_pose(
                        views, nb_img, downscale)

                    # Load mask
                    view_ids = [str(v["viewId"]) for v in views]
                    mask = find_mask_for_pose(
                        pose_id, mask_folder if mask_folder else None,
                        view_ids, views=views)

                    # Save extracted mask if needed
                    if (mask is not None and mask_output_folder
                            and not mask_folder):
                        os.makedirs(mask_output_folder, exist_ok=True)
                        import cv2
                        mask_path = os.path.join(
                            mask_output_folder,
                            "{}.png".format(pose_id))
                        cv2.imwrite(mask_path,
                                    np.uint8(mask * 255))
                        chunk.logger.info(
                            "Saved mask to {}".format(mask_path))

                    # Preprocess
                    I, mask_out, roi = preprocess_for_pose(
                        images, mask,
                        max_image_res=max_image_res)

                    # Inference
                    outputs = infer_pose(
                        I, mask_out, roi,
                        net_nml, net_brdf, target, device,
                        canonical_resolution=canonical_res,
                        pixel_samples=pixel_samples,
                        scalable=scalable)

                    # Save outputs
                    if outputs.get("normal") is not None:
                        nml_path = os.path.join(
                            output_folder,
                            "{}_normals.png".format(pose_id))
                        save_normal_16bit(
                            outputs["normal"], nml_path)

                    if outputs.get("albedo") is not None:
                        save_color_16bit(
                            outputs["albedo"],
                            os.path.join(output_folder,
                                         "{}_albedo.png".format(
                                             pose_id)))

                    if outputs.get("roughness") is not None:
                        save_gray_16bit(
                            outputs["roughness"],
                            os.path.join(output_folder,
                                         "{}_roughness.png".format(
                                             pose_id)))

                    if outputs.get("metallic") is not None:
                        save_gray_16bit(
                            outputs["metallic"],
                            os.path.join(output_folder,
                                         "{}_metallic.png".format(
                                             pose_id)))

                    results.append({
                        "poseId": pose_id,
                        "viewId": str(views[0].get("viewId")),
                        "nbImages": len(images),
                    })

                    chunk.logger.info(
                        "Pose {} done".format(pose_id))

                except Exception as e:
                    chunk.logger.warning(
                        "Failed on pose {}: {}".format(pose_id, e))
                    import traceback
                    chunk.logger.warning(traceback.format_exc())
                    continue

            total_time = time.time() - total_start
            chunk.logger.info(
                "All poses processed in {:.1f}s".format(total_time))

            # Create output SfMData files
            if target in ("normal", "normal_and_brdf"):
                self._create_output_sfm(
                    sfm_data, output_folder,
                    "normalMaps", "_normals.png", chunk.logger,
                    downscale=downscale)

            if target in ("brdf", "normal_and_brdf"):
                self._create_output_sfm(
                    sfm_data, output_folder,
                    "albedoMaps", "_albedo.png", chunk.logger,
                    downscale=downscale)
                self._create_output_sfm(
                    sfm_data, output_folder,
                    "roughnessMaps", "_roughness.png",
                    chunk.logger, downscale=downscale)
                self._create_output_sfm(
                    sfm_data, output_folder,
                    "metallicMaps", "_metallic.png",
                    chunk.logger, downscale=downscale)

        finally:
            # GPU cleanup
            try:
                import gc
                import torch as _torch
                gc.collect()
                if _torch.cuda.is_available():
                    _torch.cuda.empty_cache()
            except Exception:
                pass
            chunk.logManager.end()
