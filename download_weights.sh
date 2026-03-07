#!/bin/bash
# Download SDM-UniPS pretrained checkpoints
#
# Downloads normal and BRDF model weights from Dropbox
# into the checkpoint/ directory of this plugin.
#
# Usage:
#   cd mrSDMUniPS
#   bash download_weights.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECKPOINT_DIR="${SCRIPT_DIR}/checkpoint"
ZIP_URL="https://www.dropbox.com/s/yu8h6g0zp07mumd/checkpoint.zip?dl=1"
ZIP_FILE="/tmp/sdm_unips_checkpoint.zip"

echo "=== SDM-UniPS Checkpoint Download ==="

# Check if already downloaded
if [ -f "${CHECKPOINT_DIR}/normal/nml.pytmodel" ] && [ -f "${CHECKPOINT_DIR}/brdf/brdf.pytmodel" ]; then
    echo "Checkpoints already present in ${CHECKPOINT_DIR}"
    echo "  normal/nml.pytmodel: $(du -h "${CHECKPOINT_DIR}/normal/nml.pytmodel" | cut -f1)"
    echo "  brdf/brdf.pytmodel:  $(du -h "${CHECKPOINT_DIR}/brdf/brdf.pytmodel" | cut -f1)"
    echo "To re-download, remove the checkpoint/ directory first."
    exit 0
fi

echo "Downloading checkpoints from Dropbox (~480 MB)..."
curl -L -o "${ZIP_FILE}" "${ZIP_URL}"

echo "Extracting to ${CHECKPOINT_DIR}..."
mkdir -p "${CHECKPOINT_DIR}"
unzip -o "${ZIP_FILE}" -d "${SCRIPT_DIR}/"

# Cleanup
rm -f "${ZIP_FILE}"

# Verify
if [ -f "${CHECKPOINT_DIR}/normal/nml.pytmodel" ] && [ -f "${CHECKPOINT_DIR}/brdf/brdf.pytmodel" ]; then
    echo ""
    echo "Download complete:"
    echo "  ${CHECKPOINT_DIR}/normal/nml.pytmodel"
    echo "  ${CHECKPOINT_DIR}/brdf/brdf.pytmodel"
else
    echo "ERROR: Expected files not found after extraction."
    echo "Check that the zip contains checkpoint/normal/nml.pytmodel and checkpoint/brdf/brdf.pytmodel"
    exit 1
fi
