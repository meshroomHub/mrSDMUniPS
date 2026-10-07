# mrSDMUniPS

Meshroom plugin for [SDM-UniPS](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023/tree/meshroom) (CVPR2023) -- universal photometric stereo for surface normal and BRDF estimation.

## Quick Start

> **Prerequisite:** a working [Meshroom](https://github.com/alicevision/Meshroom) installation (2025+).

### 1. Clone the plugin

```bash
cd /path/to/your/plugins
git clone https://github.com/meshroomHub/mrSDMUniPS.git
cd mrSDMUniPS
```

### 2. Set up the virtual environment

Meshroom looks for a folder named **`venv`** at the plugin root.

```bash
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install torch torchvision
pip install -r requirements.txt

deactivate
```

This installs SDM-UniPS and all its dependencies automatically via pip.

### 3. Download pretrained weights

```bash
bash download_weights.sh
```

This downloads the pretrained checkpoints (~480 MB) from Dropbox into `checkpoint/`:

```
checkpoint/
├── normal/
│   └── nml.pytmodel
└── brdf/
    └── brdf.pytmodel
```

The plugin auto-detects this directory. No config.json needed.

### 4. Register the plugin in Meshroom

```bash
export MESHROOM_PLUGINS_PATH=/path/to/your/plugins/mrSDMUniPS:$MESHROOM_PLUGINS_PATH
```

Launch Meshroom: the **SDMUniPS** node appears under **Photometric Stereo**.

## Usage

### Input

- **SfMData** whose views sharing a poseId are the lighting images of a pose (as created by CameraInit for multi-lighting folders), e.g. the undistorted images of ExportImages. Poses with fewer than `minViewsPerPose` views (photogrammetry images) are ignored, so a mixed multi-view / multi-light SfMData can be used as is.
- **Masks** (optional): a folder of `<poseId>.png` (one mask per pose) or `<viewId>.png` (one mask per image, combined by vote); without mask files, the masks are extracted from the alpha channel of the images.

## Node Parameters

The data handling (SfMData, image selection, masks, outputs) is implemented in `psCommon.py`, a common layer shared
as an identical copy by the LINOUniPS, UniMSPS and SDMUniPS nodes: the three nodes have the same inputs, outputs and
behaviour, only the network differs.

### Inputs

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

### Outputs

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

## Advanced: Developer Setup

If you prefer to work from a local SDM-UniPS clone instead of pip install:

1. Clone the repo: `git clone -b meshroom https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023.git`
2. Edit `meshroom/config.json`:
   ```json
   [
       {"key": "SDM_UNIPS_PATH", "type": "path", "value": "/path/to/SDM-UniPS-CVPR2023"},
       {"key": "SDM_UNIPS_CHECKPOINT_PATH", "type": "path", "value": "/path/to/SDM-UniPS-CVPR2023/checkpoint"}
   ]
   ```

The node tries pip imports first (`meshroom_predict` module), then falls back to the config path. To use a local clone
in the plugin environment: `venv/bin/python -m pip install --no-deps -e /path/to/SDM-UniPS-CVPR2023`.

### Tests

```bash
# unit tests (CPU), from the plugin root
PYTHONPATH=/path/to/Meshroom venv/bin/python -m pytest tests
# one real pose (GPU): checks sizes, mask coverage and the OpenGL frame of the normals
PYTHONPATH=/path/to/Meshroom venv/bin/python tests/check_real_pose.py <sfm> <poseId> <outputFolder> --downscale 2
```

## Acknowledgements

This work is supported by [**DOPAMIn**](https://www.cnrsinnovation.com/actualite/une-seconde-promotion-pour-le-programme-open-7-nouveaux-logiciels-scientifiques-a-valoriser/) (*Diffusion Open de Photogrammetrie par AliceVision/Meshroom pour l'Industrie*), selected in the 2024 cohort of the [**OPEN**](https://www.cnrsinnovation.com/open/) programme run by [CNRS Innovation](https://www.cnrsinnovation.com/). OPEN supports the valorization of open-source scientific software by providing dedicated developer resources, governance expertise, and industry partnership support.

**Lead researcher:** [Jean-Denis Durou](https://cv.hal.science/jean-denis-durou), [IRIT](https://www.irit.fr/) (INP-Toulouse)
**Co-lead:** [Lilian Calvet](https://fr.linkedin.com/in/lilian-calvet-42b1a689), [Balgrist University Hospital](https://www.balgrist.ch/)

---

## Related Projects

| Project | Description |
|---------|-------------|
| [SDM-UniPS](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023) | Scalable, Detailed and Mask-free Universal Photometric Stereo (CVPR 2023) |
| [mrOpenRNb](https://github.com/meshroomHub/mrOpenRNb) | Meshroom plugin for neural surface reconstruction from normals |
| [mrLINOUniPS](https://github.com/meshroomHub/mrLINOUniPS) | Meshroom plugin for LINO_UniPS photometric stereo |
| [mrUniMSPS](https://github.com/meshroomHub/mrUniMSPS) | Meshroom plugin for Uni-MS-PS photometric stereo |

---

## References

Ikehata, S. "Scalable, Detailed and Mask-free Universal Photometric Stereo." CVPR 2023.

---

## License

This project is licensed under the [Mozilla Public License 2.0](LICENSE).
