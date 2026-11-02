# mrSDMUniPS

Meshroom plugin for [SDM-UniPS](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023): scalable, detailed and
mask-free universal photometric stereo (S. Ikehata, CVPR 2023).

SDM-UniPS estimates per-pixel surface normals and BRDF maps from multi-lighting images, without known light directions.
The node is harmonized with the other photometric stereo plugins (mrLINOUniPS, mrUniMSPS, mrLedGetter, through the shared
`psCommon.py` layer), and its outputs are ready for RNb-NeuS2:

| Node | Step | Output |
|------|------|--------|
| `SDMUniPS` | Normals and BRDF maps per pose | normal maps, masks, albedo, roughness and metallic maps, `normalMaps.sfm`, `albedoMaps.sfm` |

---

## Requirements

- **[Meshroom](https://github.com/alicevision/Meshroom)** 2026.1 or later (develop branch until its release, tested on
  commit [`edc4b6a2`](https://github.com/alicevision/Meshroom/commit/edc4b6a2)): Meshroom 2025.1.x has neither the plugin
  manager nor the `[tool.meshroom]` settings of `pyproject.toml`
- **NVIDIA GPU** with a driver supporting CUDA 12.1
- **Python** 3.10 or newer

All Python dependencies are declared in [`pyproject.toml`](pyproject.toml): PyTorch (CUDA 12.1) and `sdm-unips`, pinned to the
`weights-v1` tag of [meshroomHubWarehouse/SDM-UniPS-CVPR2023](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023), a fork of
[satoshi-ikehata/SDM-UniPS-CVPR2023](https://github.com/satoshi-ikehata/SDM-UniPS-CVPR2023).

---

## Installation

### 1. Install the plugin

From Meshroom's plugin manager (*Manage Plugins*), or from the command line:

```bash
meshroom_plugins install mrSDMUniPS
```

The installer creates the plugin `venv/` with `uv sync` and downloads the pretrained checkpoints (~503 MB), declared as assets in `pyproject.toml`, checking their SHA-256.
The `SDMUniPS` node then appears in the *Photometric Stereo* category.

### 2. Manual install (without the plugin manager)

Requires [uv](https://docs.astral.sh/uv/).

```bash
cd /path/to/plugins
git clone https://github.com/meshroomHub/mrSDMUniPS.git
cd mrSDMUniPS
UV_PROJECT_ENVIRONMENT=venv uv sync   # Meshroom looks for venv/ at the plugin root

URL=https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023/releases/download/weights-v1
mkdir -p checkpoint/normal checkpoint/brdf
curl -L -o checkpoint/normal/nml.pytmodel $URL/nml.pytmodel
curl -L -o checkpoint/brdf/brdf.pytmodel $URL/brdf.pytmodel
echo "100747de145238f40c1ff1e1263ce2bd3d7d7b12d15214a6acba1134ed937bff  checkpoint/normal/nml.pytmodel" | sha256sum -c
echo "9322b017cac0a2de81f009a206d5d94e609cae2997abdd1dc2dac912e4eaf910  checkpoint/brdf/brdf.pytmodel" | sha256sum -c

export MESHROOM_PLUGINS_PATH=/path/to/plugins/mrSDMUniPS:$MESHROOM_PLUGINS_PATH
```

On Windows (PowerShell): `$env:UV_PROJECT_ENVIRONMENT = "venv"; uv sync`, then
`$env:MESHROOM_PLUGINS_PATH = "C:\path\to\plugins\mrSDMUniPS"`.

These are the files of the `checkpoint.zip` linked from the
[SDM-UniPS](https://github.com/satoshi-ikehata/SDM-UniPS-CVPR2023) README, mirrored one by one.

---

## Pipeline template

`meshroom/sdmUniPs.mgt` (*File > New Pipeline > Sdm Uni Ps*) runs the structure-from-motion of AliceVision, segments the
object with SAM 3, exports the undistorted images and estimates the normals and the BRDF maps with `SDMUniPS`.

It needs [mrSegmentation](https://github.com/meshroomHub/mrSegmentation) (node `ImageSegmentationSam3`), not in the plugin
registry yet: install it by hand.

Images: one folder per pose, holding the single-light images and one reference image lit by all the lights, whose
filename contains `ambient` (CameraInit makes it the pose reference) and `all_leds` (`SfMFilter_1` keeps these images
for the structure from motion and the segmentation). Set the SAM 3 prompt (`ImageSegmentationSam3_1`, default `stone`)
to your object.

---

## Nodes

### `SDMUniPS`

- **SfMData** whose views sharing a poseId are the lighting images of a pose (as created by CameraInit for multi-lighting folders), e.g. the undistorted images of ExportImages. Poses with fewer than `minViewsPerPose` views (photogrammetry images) are ignored, so a mixed multi-view / multi-light SfMData can be used as is.
- **Masks** (optional): a folder of `<poseId>.png` (one mask per pose) or `<viewId>.png` (one mask per image, combined by vote); without mask files, the masks are extracted from the alpha channel of the images.

The data handling (SfMData, image selection, masks, outputs) is implemented in `psCommon.py`, a common layer shared
as an identical copy by the LINOUniPS, UniMSPS and SDMUniPS nodes: the three nodes have the same inputs, outputs and
behaviour, only the network differs.

#### Inputs

| Parameter | Label | Default | Description |
|-----------|-------|---------|-------------|
| `inputSfm` | SfMData | | SfMData whose views sharing a poseId are the lighting images of a pose (e.g. ExportImages output) **(required)** |
| `maskFolder` | Mask Folder | | Masks `<poseId>.png` (one per pose) or `<viewId>.png` (one per image, combined by vote); alpha channels otherwise |
| `downscale` | Downscale Factor | 1 | Integer downscale factor of the images (and of the output maps and intrinsics) |
| `nbImages` | Number Of Images | -1 | Maximum number of lighting images per pose (-1: all); the GPU memory grows with it |
| `target` | Target | `normal_and_brdf` | `normal`, `brdf` or `normal_and_brdf`; the normal maps are always estimated (they define the support of every map) |
| `outputFormat` | Output Format | `png16` | `png16` (16-bit PNG, (n + 1) / 2) or `exr` (float32) |
| `useGpu` | Use GPU | true | Use the GPU (CPU otherwise) |

Advanced inputs, common to the three nodes:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `minViewsPerPose` | 3 | Minimum number of views of a pose to process it (photogrammetry views are ignored) |
| `imageSelection` | `random` | Choice of the images when `nbImages` is lower than the number of images: `random`, `uniform`, `first` |
| `seed` | 42 | Seed of the random selection and of the network, combined with the poseId (reproducible per pose) |
| `linearizeInput` | false | Convert 8/16-bit images from sRGB to linear values |
| `maskThreshold` | 0.5 | Binarization of the masks and alpha channels, as a fraction of the value range |
| `maskVoteThreshold` | 0.5 | A pixel is in the pose mask when the fraction of per-image masks containing it is greater than this value (0.5: strict majority, 1: intersection, 0: union) |
| `maskRemoveBorderComponents` | true | Remove the alpha mask components touching the image border (valid area of undistorted images) |
| `maskUseGlobalFile` | false | Use `<maskFolder>/mask.png` for the poses without a specific mask |
| `normalConvention` | `opengl` | Output frame: `opengl` (x right, y up, z towards the camera, expected by RNb-NeuS2) or `opencv` |
| `keepLandmarks` | true | Keep the 3D landmarks in the output SfMData |
| `failurePolicy` | `noPose` | Fail if no pose could be processed (`noPose`), if any pose failed (`anyPose`), or `never` |

Advanced inputs specific to SDM-UniPS:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cropMargin` | 8 | Margin around the mask bounding box (the whole image is used when the box is closer to the border) |
| `maxProcessingSize` | 4096 | Maximum side of the square network input (multiple of 512): `max(512, min(maxProcessingSize, floor(crop side / 512) * 512))` |
| `canonicalResolution` | 256 | Resolution of the global image encoder: 128, 256 (training resolution) or 512 |
| `pixelSamples` | 10000 | Number of pixels decoded together by the pixel-sampling transformer |
| `scalable` | true | Process the network input as 512x512 interleaved sub-grids, one at a time; disabled (original default), the whole input is processed at once and needs much more GPU memory (9 images at 1536x1536 do not fit in 16 GB) |
| `outputInterpolation` | `cubic` | Resampling of the prediction back to the crop size: `area`, `linear`, `cubic` |
| `modelPath` | | Checkpoint folder (`normal/` and `brdf/`, one `.pytmodel` each); default: `checkpoint/` of the plugin, then `$SDM_UNIPS_CHECKPOINT_PATH`, then `checkpoint/` of SDM-UniPS |
| `sdmUniPsPath` | `${SDM_UNIPS_PATH}` | SDM-UniPS code, used when the package is not installed in the plugin environment |

The network itself is unchanged; its pre/post-processing (`meshroom_predict.py` of SDM-UniPS) follows the original
code (crop with margin, square network input, per-image normalization by the maximum over the mask), with float
inputs, the scalable mode by default, the whole image processed when there is no mask (instead of a centered
square) and the maps multiplied by the pose mask. The network outputs normals in the OpenGL camera frame (checked on
real data). The pixel sampling is seeded per pose (`seed`).

#### Outputs

| Parameter | Description |
|-----------|-------------|
| `outputFolder` | Normal maps `<poseId>.png` (or `.exr`), pose masks `masks/<poseId>.png`, BRDF maps `albedo/`, `roughness/`, `metallic/<poseId>.png` (or `.exr`) |
| `outputSfmDataNormal` | SfMData referencing the normal maps: one view per pose (the view whose viewId is the poseId), intrinsics scaled by `downscale` |
| `outputSfmDataAlbedo`, `outputSfmDataRoughness`, `outputSfmDataMetallic` | SfMData referencing the BRDF maps (written when `target` includes `brdf`) |
| `outputMaskFolder` | Pose masks (0/255): the pixels where a normal is defined |

The BRDF maps are zero outside the pose mask. The albedo is relative: each input image is normalized by its own
maximum, so its scale is not comparable between poses.

Downscaling keeps the camera model exact: the downscaled pixel `i` averages the input pixels `[i * d, (i + 1) * d)`,
so the principal point becomes `(pp + 0.5) / d - 0.5` (AliceVision puts the center of pixel `i` at `i`).

---

## Development

### Tests

```bash
# unit tests (CPU), from the plugin root
PYTHONPATH=/path/to/Meshroom venv/bin/python -m pytest tests
# one real pose (GPU): checks sizes, mask coverage and the OpenGL frame of the normals
PYTHONPATH=/path/to/Meshroom venv/bin/python tests/check_real_pose.py <sfm> <poseId> <outputFolder> --downscale 2
```

### Working on a local SDM-UniPS clone

The node imports SDM-UniPS from the plugin `venv/`. To run a local clone instead, install it in editable mode in that venv:

```bash
uv pip install --python venv/bin/python -e /path/to/SDM-UniPS-CVPR2023
```

Updating or reinstalling the plugin from the plugin manager recreates `venv/`: run this command again afterwards.

`SDM_UNIPS_PATH` (an environment variable, or the `sdmUniPsPath` input of the node) is only a fallback: the node uses it
when SDM-UniPS is not installed in the venv. Checkpoints elsewhere: `modelPath` input, or `SDM_UNIPS_CHECKPOINT_PATH`.

### Plugin structure

```
mrSDMUniPS/
├── meshroom/
│   ├── sdmUniPs.mgt               # Pipeline template
│   └── SDM-UniPS/
│       ├── __init__.py
│       ├── SDM-UniPS.py           # Meshroom node definition
│       └── psCommon.py            # Common photometric stereo layer (identical in mrLINOUniPS, mrUniMSPS)
├── tests/                         # pytest tests (CPU) + check_real_pose.py (GPU check on a real pose)
├── checkpoint/                    # Model weights (Meshroom asset)
│   ├── normal/nml.pytmodel
│   └── brdf/brdf.pytmodel
├── venv/                          # Created by the installer or by uv sync
├── pyproject.toml                 # Dependencies and Meshroom settings (uv)
└── README.md
```

For more details on how Meshroom plugins work, see:
- [Meshroom Plugin Install Guide](https://github.com/alicevision/Meshroom/blob/develop/INSTALL_PLUGINS.md)
- [mrHelloWorld](https://github.com/meshroomHub/mrHelloWorld): step-by-step tutorials for building Meshroom plugins

---

## Acknowledgements

This work is supported by [**DOPAMIn**](https://www.cnrsinnovation.com/actualite/une-seconde-promotion-pour-le-programme-open-7-nouveaux-logiciels-scientifiques-a-valoriser/) (*Diffusion Open de Photogrammetrie par AliceVision/Meshroom pour l'Industrie*), selected in the 2024 cohort of the [**OPEN**](https://www.cnrsinnovation.com/open/) programme run by [CNRS Innovation](https://www.cnrsinnovation.com/). OPEN supports the valorization of open-source scientific software by providing dedicated developer resources, governance expertise, and industry partnership support.

**Lead researcher:** [Jean-Denis Durou](https://cv.hal.science/jean-denis-durou), [IRIT](https://www.irit.fr/) (INP-Toulouse)
**Co-lead:** [Lilian Calvet](https://fr.linkedin.com/in/lilian-calvet-42b1a689), [Balgrist University Hospital](https://www.balgrist.ch/)

---

## Related Projects

| Project | Description |
|---------|-------------|
| [SDM-UniPS](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023) | Scalable, Detailed and Mask-free Universal Photometric Stereo (CVPR 2023) |
| [mrLINOUniPS](https://github.com/meshroomHub/mrLINOUniPS) | Meshroom plugin for LINO-UniPS photometric stereo |
| [mrUniMSPS](https://github.com/meshroomHub/mrUniMSPS) | Meshroom plugin for Uni-MS-PS photometric stereo |
| [mrLedGetter](https://github.com/meshroomHub/mrLedGetter) | Meshroom plugin for LED-getter near-light photometric stereo |
| [mrRNbNeuS2](https://github.com/meshroomHub/mrRNbNeuS2) | Meshroom plugin for RNb-NeuS2 neural surface reconstruction |
| [mrOpenRNb](https://github.com/meshroomHub/mrOpenRNb) | Meshroom plugin for Open-RNb neural surface reconstruction |

---

## Citation

- **Scalable, Detailed and Mask-free Universal Photometric Stereo**  
  S. Ikehata (2023)  
  In *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*.

---

## License

This project is licensed under the [Mozilla Public License 2.0](LICENSE).
