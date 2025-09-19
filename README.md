# mrSDMUniPS

A Meshroom node integration for [**SDM-UniPS: Scalable, Detailed, and Mask-Free Universal Photometric Stereo**](https://github.com/satoshi-ikehata/SDM-UniPS-CVPR2023) (CVPR2023 Highlight).

## Overview

This project provides a Meshroom node wrapper for the SDM-UniPS neural network, enabling seamless integration of universal photometric stereo reconstruction into the Meshroom pipeline. SDM-UniPS can recover intricate surface normal maps and BRDF parameters (albedo, roughness, metallic) from images captured under unknown, spatially-varying lighting conditions.

**Key Features:**
- **Universal Photometric Stereo**: Works with arbitrary lighting conditions without calibration
- **Mask-free Processing**: No object masks required (though optional masks are supported)
- **High-quality Results**: Rivals 3D scanner quality for surface normal estimation
- **BRDF Recovery**: Estimates albedo, roughness, and metallic parameters
- **Scalable Processing**: Handles high-resolution images efficiently
- **Meshroom Integration**: Seamless workflow with AliceVision SfMData format

## Installation

1. Clone this repository into your Meshroom nodes directory
2. Install the required dependencies:
```bash
cd /path/to/mrSDMUniPS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Download the pretrained models from [here](https://www.dropbox.com/s/yu8h6g0zp07mumd/checkpoint.zip?dl=0) and extract them to your checkpoint directory

## Usage

### Input Requirements

The SDMUniPS node accepts:
- **SfMData file**: AliceVision SfMData containing images and camera poses
- **Optional masks**: Directory with pose-specific masks or alpha channel images
- **Multiple images per pose**: Images captured under different lighting conditions

### Node Parameters

- **Target Output**: Choose between normal maps, BRDF parameters, or both
- **Max Image Resolution**: Maximum resolution for processing (default: 4096)
- **Max Images per Pose**: Limit number of images processed per pose (default: 10)
- **Scalable Mode**: Enable for high-resolution processing with reduced memory usage
- **Enable Cropping**: Automatic cropping based on mask bounding boxes
- **Checkpoint Path**: Path to the pretrained model files

### Output Files

The node generates:
- **Normal Maps**: Surface normals in camera coordinate system (`<POSE_ID>_normals.exr`)
- **Albedo Maps**: Base color maps (`<POSE_ID>_albedo.png`)
- **Roughness Maps**: Surface roughness parameters (`<POSE_ID>_roughness.png`)
- **Metallic Maps**: Metallic parameters (`<POSE_ID>_metallic.png`)
- **SfMData files**: Updated SfMData with output image references

<!-- ### Directory Structure

The node automatically organizes data for SDM-UniPS processing:
```
output_directory/
├── sdm_unips_data/
│   ├── pose_0.data/
│   │   ├── L000.jpg
│   │   ├── L001.jpg
│   │   └── mask.png (optional)
│   └── pose_1.data/
│       ├── L000.jpg
│       └── L001.jpg
└── results/
    ├── pose_0_normals.exr
    ├── pose_0_albedo.png
    └── ...
``` -->

## ⚠️ Work in Progress (WIP)

### Known Issues

1. **Intrinsics Not Updated After Cropping**: When cropping is enabled, the camera intrinsics in the output SfMData are not automatically updated to reflect the new image dimensions and principal point. This needs to be implemented to maintain proper camera calibration.

2. **Output Bug**: There is currently a bug in the output generation that prevents the node from working properly. The node is under active development to resolve this issue.

### TODO
- [ ] Update camera intrinsics after cropping operations
- [ ] Fix output generation bug

## References

**Original Paper:**
```bibtex
@inproceedings{ikehata2023sdmunips,
  title={Scalable, Detailed and Mask-free Universal Photometric Stereo},
  author={Satoshi Ikehata},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2023}
}
```

**Links:**
- [Original Repository](https://github.com/satoshi-ikehata/SDM-UniPS-CVPR2023)
- [Paper (ArXiv)](https://arxiv.org/abs/2303.15724)
- [Author's Page](https://satoshi-ikehata.github.io/)
- [Pretrained Models](https://www.dropbox.com/s/yu8h6g0zp07mumd/checkpoint.zip?dl=0)
- [Sample Data](https://www.dropbox.com/sh/afm4lkiz0iu1un3/AACfdKB66wl8iyFtJ4fzynGYa?dl=0)
