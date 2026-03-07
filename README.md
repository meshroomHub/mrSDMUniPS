# mrSDMUniPS

Meshroom plugin for [SDM-UniPS](https://github.com/meshroomHubWarehouse/SDM-UniPS-CVPR2023/tree/meshroomMain) (CVPR2023) -- universal photometric stereo for surface normal and BRDF estimation.

## Setup

### config.json

The plugin requires two paths configured in `meshroom/config.json`:

- **SDM_UNIPS_PATH** -- path to the SDM-UniPS source directory (must contain `inference_sfm.py`)
- **SDM_UNIPS_CHECKPOINT_PATH** -- path to the pretrained checkpoint directory (defaults to `../checkpoint`)

### Checkpoints

Download pretrained models from [Dropbox](https://www.dropbox.com/s/yu8h6g0zp07mumd/checkpoint.zip?dl=0) and extract them to the checkpoint directory.

## Usage

### Input

- **SfMData JSON** with multi-lighting views grouped by poseId (multiple images per pose, each under different lighting)
- **Mask folder** (optional) with mask PNGs named by poseId (e.g. `12345.png`)

### Output

- **Normal maps** -- surface normals per pose (`<poseId>_normals.png`)
- **Albedo maps** -- base color per pose (`<poseId>_albedo.png`)
- **Roughness maps** -- surface roughness per pose (`<poseId>_roughness.png`)
- **Metallic maps** -- metallic parameter per pose (`<poseId>_metallic.png`)
- **Output SfMData files** -- `normalMaps.sfm`, `albedoMaps.sfm`, `roughnessMaps.sfm`, `metallicMaps.sfm`

## References

Ikehata, S. "Scalable, Detailed and Mask-free Universal Photometric Stereo." CVPR 2023.
