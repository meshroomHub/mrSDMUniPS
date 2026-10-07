"""Unit tests of the SDM-UniPS Meshroom API (meshroom_predict.py of SDM-UniPS), CPU only, with fake networks.

Run from the plugin root (SDM-UniPS installed in the plugin venv):
    PYTHONPATH=<Meshroom> venv/bin/python -m pytest tests
"""
import os

import numpy as np
import pytest
import torch

api = pytest.importorskip("meshroom_predict")

NORMAL = np.array([0.6, 0.0, 0.8], np.float32)


class FakeNet:
    """Network returning constant maps where the mask is set (the real networks write zeros elsewhere), and
    recording its inputs."""

    def __init__(self):
        self.pixel_samples = None
        self.inputs = []

    def __call__(self, images, mask, nbImages, decoder_resolution, canonical_resolution):
        self.inputs.append((images.clone(), mask.clone(), int(decoder_resolution[0, 0]),
                            int(canonical_resolution[0, 0])))
        batch, _, height, width, _ = images.shape
        ones = torch.ones((batch, 1, height, width)) * (mask > 0)
        normal = torch.from_numpy(NORMAL).reshape(1, 3, 1, 1) * ones
        return normal, 0.5 * ones.expand(-1, 3, -1, -1), 0.25 * ones, 0.75 * ones


def fakeModel(normal=True, brdf=True):
    return api.SdmModel(FakeNet() if normal else None, FakeNet() if brdf else None, "cpu")


def diskMask(height=300, width=400, center=(140, 220), radius=90):
    rows, cols = np.mgrid[:height, :width]
    return (rows - center[0]) ** 2 + (cols - center[1]) ** 2 <= radius ** 2


def images(mask, nb=4):
    rng = np.random.default_rng(0)
    return [rng.uniform(0.0, 0.5 + i, mask.shape + (3,)).astype(np.float32) for i in range(nb)]


# ---------------------------------------------------------------------------------------------- options

def test_check_options_defaults():
    api.checkOptions()
    api.checkOptions(maxProcessingSize=1024, canonicalResolution=512, scalable=True, outputInterpolation="area")


@pytest.mark.parametrize("options", [
    dict(canonicalResolution=300), dict(canonicalResolution=1024), dict(maxProcessingSize=1000),
    dict(maxProcessingSize=256), dict(pixelSamples=0), dict(cropMargin=-1), dict(outputInterpolation="nearest"),
])
def test_check_options_invalid(options):
    with pytest.raises(ValueError):
        api.checkOptions(**options)


def test_predict_rejects_invalid_options():
    mask = diskMask()
    with pytest.raises(ValueError):
        api.predict(fakeModel(), images(mask), mask, canonicalResolution=300)


# ---------------------------------------------------------------------------------------------- checkpoints

def test_load_model_missing_checkpoint(tmp_path):
    with pytest.raises(RuntimeError, match="not found"):
        api.loadModel(str(tmp_path / "missing"), useGpu=False)
    with pytest.raises(RuntimeError, match="exactly one"):
        api.loadModel(str(tmp_path), useGpu=False, target="normal")


def test_load_model_ambiguous_checkpoint(tmp_path):
    os.makedirs(tmp_path / "normal")
    for name in ("a.pytmodel", "b.pytmodel"):
        (tmp_path / "normal" / name).write_bytes(b"")
    with pytest.raises(RuntimeError, match="exactly one"):
        api.loadModel(str(tmp_path), useGpu=False, target="normal")
    # the brdf target only needs the brdf checkpoint
    with pytest.raises(RuntimeError, match="brdf"):
        api.loadModel(str(tmp_path), useGpu=False, target="brdf")


def test_load_model_incomplete_checkpoint(tmp_path):
    os.makedirs(tmp_path / "normal")
    torch.save({"module.regressor.prediction_normal.regression.2.bias": torch.zeros(3)},
               str(tmp_path / "normal" / "nml.pytmodel"))
    with pytest.raises(RuntimeError, match="Invalid SDM-UniPS normal checkpoint"):
        api.loadModel(str(tmp_path), useGpu=False, target="normal")


def test_load_model_unknown_target(tmp_path):
    with pytest.raises(ValueError):
        api.loadModel(str(tmp_path), useGpu=False, target="albedo")


# ---------------------------------------------------------------------------------------------- geometry

def test_crop_box_square_with_margin():
    mask = np.zeros((300, 400), bool)
    mask[100:150, 200:300] = True  # 50 x 100 box
    r0, r1, c0, c1 = api.cropBox(mask, 8)
    assert (c0, c1) == (192, 308)
    assert r1 - r0 == c1 - c0 and r0 <= 92 and r1 >= 158  # rows extended to a square


def test_crop_box_inclusive_without_margin():
    mask = np.zeros((300, 400), bool)
    mask[100:150, 100:150] = True
    assert api.cropBox(mask, 0) == (100, 150, 100, 150)


@pytest.mark.parametrize("box", [(0, 50, 100, 150), (100, 150, 395, 400)])
def test_crop_box_whole_image_near_border(box):
    mask = np.zeros((300, 400), bool)
    mask[box[0]:box[1], box[2]:box[3]] = True
    assert api.cropBox(mask, 8) == (0, 300, 0, 400)


def test_crop_box_no_mask_whole_image():
    assert api.cropBox(np.ones((300, 400), bool), 8) == (0, 300, 0, 400)
    assert api.cropBox(np.ones((300, 400), bool), 0) == (0, 300, 0, 400)


def test_processing_size():
    assert api.processingSize(300, 400, 4096) == 512
    assert api.processingSize(1100, 1023, 4096) == 1024
    assert api.processingSize(9000, 100, 4096) == 4096


# ---------------------------------------------------------------------------------------------- predict

def test_predict_maps():
    mask = diskMask()
    model = fakeModel()
    maps = api.predict(model, images(mask), mask)
    assert set(maps) == {"normal", "albedo", "roughness", "metallic"}
    normal = maps["normal"]
    assert normal.shape == mask.shape + (3,) and normal.dtype == np.float32
    assert not normal[~mask].any() and not maps["albedo"][~mask].any()
    norms = np.linalg.norm(normal, axis=2)
    assert np.allclose(norms[norms > 0], 1.0, atol=1e-5)
    assert (norms[mask] > 0).mean() > 0.99  # the normals cover the mask
    assert np.allclose(normal[norms > 0], NORMAL * api.NATIVE_TO_OPENGL, atol=1e-5)
    # BRDF maps resampled with the network mask as weight: no dark fringe along the silhouette
    assert maps["roughness"].shape == mask.shape and maps["albedo"].shape == mask.shape + (3,)
    inside = mask & (norms > 0)
    assert np.allclose(maps["albedo"][inside], 0.5, atol=1e-3)
    assert np.allclose(maps["roughness"][inside], 0.25, atol=1e-3)
    assert np.allclose(maps["metallic"][inside], 0.75, atol=1e-3)


def test_predict_network_inputs():
    mask = diskMask()
    model = fakeModel(brdf=False)
    model.netNormal.pixel_samples = None
    maps = api.predict(model, images(mask, nb=3), mask, canonicalResolution=128, pixelSamples=2000)
    assert set(maps) == {"normal"}
    netImages, netMask, resolution, canonical = model.netNormal.inputs[0]
    assert netImages.shape == (1, 3, 512, 512, 3) and netMask.shape == (1, 1, 512, 512)
    assert (resolution, canonical, model.netNormal.pixel_samples) == (512, 128, 2000)
    # per-image normalization: maximum over the mask of the mean RGB value = 1
    brightness = netImages[0].mean(dim=0)[netMask[0, 0] > 0]
    assert torch.allclose(brightness.max(dim=0).values, torch.ones(3), atol=1e-4)


def test_predict_scalable_matches():
    mask = diskMask(1100, 1200, (550, 600), 520)  # crop 1057 px: 1024 x 1024 input
    model = fakeModel()
    full = api.predict(model, images(mask, nb=2), mask, scalable=False)
    assert model.netNormal.inputs[-1][0].shape[2:4] == (1024, 1024)
    tiled = api.predict(model, images(mask, nb=2), mask)  # scalable by default
    assert model.netNormal.inputs[-1][0].shape[2:4] == (512, 512)  # 1024 input processed as 4 sub-grids
    for name in full:
        assert np.allclose(full[name], tiled[name], atol=1e-5), name


def test_predict_without_mask_whole_image():
    mask = np.ones((300, 400), bool)
    normal = api.predict(fakeModel(brdf=False), images(mask), mask)["normal"]
    assert (np.linalg.norm(normal, axis=2) > 0).all()  # the original code only processed a centered square


def test_predict_input_errors():
    mask = diskMask()
    with pytest.raises(ValueError):
        api.predict(fakeModel(), [], mask)
    with pytest.raises(ValueError):
        api.predict(fakeModel(), [np.zeros((10, 10, 3), np.float32)], mask)
    with pytest.raises(ValueError):
        api.predict(fakeModel(), images(mask), np.zeros_like(mask))
    with pytest.raises(RuntimeError):
        api.predict(api.SdmModel(None, None, "cpu"), images(mask), mask)
