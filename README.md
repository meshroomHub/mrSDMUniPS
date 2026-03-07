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

- **SfMData JSON** with multi-lighting views grouped by poseId (multiple images per pose, each under different lighting)
- **Mask folder** (optional) with mask PNGs named by poseId (e.g. `12345.png`)

### Output

- **Normal maps** -- surface normals per pose (`<poseId>_normals.png`)
- **Albedo maps** -- base color per pose (`<poseId>_albedo.png`)
- **Roughness maps** -- surface roughness per pose (`<poseId>_roughness.png`)
- **Metallic maps** -- metallic parameter per pose (`<poseId>_metallic.png`)
- **Output SfMData files** -- `normalMaps.sfm`, `albedoMaps.sfm`, `roughnessMaps.sfm`, `metallicMaps.sfm`

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

The node tries pip imports first, then falls back to the config path.

## References

Ikehata, S. "Scalable, Detailed and Mask-free Universal Photometric Stereo." CVPR 2023.
