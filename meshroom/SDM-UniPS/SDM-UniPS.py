__version__ = "2.0"

import os

from meshroom.core import desc

from . import psCommon

BRDF_MAPS = ("albedo", "roughness", "metallic")


class SDMUniPS(desc.Node):
    """Multi-view photometric stereo normal (and BRDF) estimation with SDM-UniPS."""

    category = "Photometric Stereo"
    gpu = desc.Level.INTENSIVE
    size = desc.DynamicNodeSize("inputSfm")

    documentation = """
Estimate one normal map per multi-lighting pose with SDM-UniPS (CVPR 2023, universal photometric stereo: unknown
lighting), and optionally the BRDF maps (albedo, roughness, metallic).

**Inputs:** an SfMData where the lighting images of a pose share the same poseId (as created by CameraInit for
multi-lighting folders), e.g. the undistorted images of ExportImages. Poses with fewer than 'Min Views Per Pose'
views (photogrammetry images) are ignored, so a mixed multi-view / multi-light SfMData can be used as is.

**Masks:** from a mask folder (<poseId>.png or <viewId>.png) or from the alpha channel of the images; the
per-image masks of a pose are combined by vote ('Mask Vote Threshold').

**Outputs:** one normal map per pose (<poseId>.png|exr, OpenGL camera frame by default), the pose masks
(masks/<poseId>.png: pixels with a normal), the BRDF maps (albedo/, roughness/, metallic/<poseId>.png|exr, zero
outside the pose mask; the albedo is relative to the brightness of each pose) and one SfMData per map type (one
view per pose, with the intrinsics scaled by the downscale factor), ready for RNb-NeuS2.

The data handling (SfMData, image selection, masks, outputs) is common to the LINOUniPS, UniMSPS and SDMUniPS
nodes; see the advanced options.
"""

    inputs = psCommon.inputAttributes() + [
        desc.ChoiceParam(
            name="target",
            label="Target",
            description="Maps to estimate:\n"
                        " - normal: normal maps.\n"
                        " - brdf: BRDF maps (albedo, roughness, metallic). The normal maps are estimated too: they "
                        "define the support of every output map.\n"
                        " - normal_and_brdf: normal and BRDF maps (same as brdf).",
            value="normal_and_brdf",
            values=["normal", "brdf", "normal_and_brdf"],
            exclusive=True,
        ),
        desc.IntParam(
            name="cropMargin",
            label="Crop Margin",
            description="Margin (pixels) around the bounding box of the mask. The whole image is processed when the "
                        "box is closer than this margin to the image border.",
            value=8,
            range=(0, 256, 1),
            advanced=True,
        ),
        desc.IntParam(
            name="maxProcessingSize",
            label="Max Processing Size",
            description="Maximum side of the square network input (multiple of 512): the crop is resized to "
                        "max(512, min(Max Processing Size, floor(crop side / 512) * 512)). "
                        "The GPU memory grows with this size (see 'Scalable').",
            value=4096,
            range=(512, 8192, 512),
            advanced=True,
        ),
        desc.ChoiceParam(
            name="canonicalResolution",
            label="Canonical Resolution",
            description="Resolution of the global image encoder (the network was trained at 256).",
            value=256,
            values=[128, 256, 512],
            exclusive=True,
            advanced=True,
        ),
        desc.IntParam(
            name="pixelSamples",
            label="Pixel Samples",
            description="Number of pixels decoded together by the pixel-sampling transformer.",
            value=10000,
            range=(1000, 100000, 1000),
            advanced=True,
        ),
        desc.BoolParam(
            name="scalable",
            label="Scalable",
            description="Process the network input as 512x512 interleaved sub-grids, one at a time. Disabled, the "
                        "whole input is processed at once (original default), which needs much more GPU memory: "
                        "the encoder processes N x (side / Canonical Resolution)^2 tiles at once (e.g. 9 images "
                        "at 1536x1536 do not fit in 16 GB).",
            value=True,
            advanced=True,
        ),
        desc.ChoiceParam(
            name="outputInterpolation",
            label="Output Interpolation",
            description="Resampling of the network prediction back to the crop size.",
            value="cubic",
            values=["area", "linear", "cubic"],
            exclusive=True,
            advanced=True,
        ),
        desc.File(
            name="modelPath",
            label="Model",
            description="SDM-UniPS checkpoint folder (with normal/ and brdf/ subfolders, one .pytmodel each). "
                        "If empty: <plugin>/checkpoint, then $SDM_UNIPS_CHECKPOINT_PATH, then "
                        "<SDM-UniPS>/checkpoint.",
            value="",
            advanced=True,
        ),
        desc.File(
            name="sdmUniPsPath",
            label="SDM-UniPS Path",
            description="SDM-UniPS code directory, used if the package is not installed in the plugin environment.",
            value="${SDM_UNIPS_PATH}",
            advanced=True,
            invalidate=False,
        ),
    ] + psCommon.advancedInputAttributes() + psCommon.settingsAttributes()

    outputs = psCommon.outputAttributes(extraMaps=BRDF_MAPS)

    @staticmethod
    def findCheckpoint(node):
        """Checkpoint folder: the 'Model' attribute, else the first existing default location."""
        if node.modelPath.value:
            return node.modelPath.value
        candidates = [os.path.join(os.path.dirname(__file__), "..", "..", "checkpoint")]
        if os.environ.get("SDM_UNIPS_CHECKPOINT_PATH"):
            candidates.append(os.environ["SDM_UNIPS_CHECKPOINT_PATH"])
        if node.sdmUniPsPath.evalValue:
            candidates.append(os.path.join(node.sdmUniPsPath.evalValue, "checkpoint"))
        for path in candidates:
            if os.path.isdir(path):
                return os.path.abspath(path)
        raise RuntimeError("SDM-UniPS checkpoint not found, set 'Model' or download it (download_weights.sh). "
                           "Searched: {}".format(", ".join(candidates)))

    @staticmethod
    def importApi(node):
        try:
            import meshroom_predict
        except ImportError:
            import sys
            path = node.sdmUniPsPath.evalValue
            if not path or not os.path.isdir(path):
                raise RuntimeError("SDM-UniPS is not installed in the plugin environment and 'SDM-UniPS Path' is "
                                   "invalid: '{}'".format(path))
            sys.path.insert(0, path)
            import meshroom_predict
        return meshroom_predict

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)
            import torch
            node = chunk.node
            api = self.importApi(node)
            options = dict(cropMargin=node.cropMargin.value, maxProcessingSize=node.maxProcessingSize.value,
                           canonicalResolution=int(node.canonicalResolution.value),
                           pixelSamples=node.pixelSamples.value, scalable=node.scalable.value,
                           outputInterpolation=node.outputInterpolation.value)
            api.checkOptions(**options)
            withBrdf = "brdf" in node.target.value
            checkpoint = self.findCheckpoint(node)
            # the normal network always runs: the normal maps define the support of every output map
            model = api.loadModel(checkpoint, useGpu=node.useGpu.value, logger=chunk.logger,
                                  target="normal_and_brdf" if withBrdf else "normal")

            def predict(images, mask):
                return api.predict(model, images, mask, **options)

            def cleanup():
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            psCommon.processPoses(chunk, predict, extraMaps=BRDF_MAPS if withBrdf else (), cleanup=cleanup)
        finally:
            chunk.logManager.end()
