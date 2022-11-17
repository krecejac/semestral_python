import math

import cv2
import pytest
import numpy as np
from scipy.signal import convolve2d
from scipy.spatial.distance import cdist
from pathlib import Path
from utils import apply_gaussian_2d
import orb


import inspect
from pylint.lint import Run
from pylint.reporters import CollectingReporter


@pytest.fixture
def linter():
    """Test codestyle for src file of orb detector."""
    src_file = inspect.getfile(orb)
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    # E1101 Module 'cv2' has no 'resize' member (no-member)
    # R0913 Too many arguments (6/5) (too-many-arguments)
    # R0914 Too many local variables (18/15) (too-many-locals)
    r = Run(
        ["--disable=C0301,C0103,E1101,R0913,R0914", "-sn", src_file],
        reporter=rep,
        exit=False,
    )
    return r.linter


@pytest.mark.parametrize("limit", range(0, 11))
def test_codestyle_score(linter, limit, runs=[]):
    """Evaluate codestyle for different thresholds."""
    if len(runs) == 0:
        print("\nLinter output:")
        for m in linter.reporter.messages:
            print(f"{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}")
    runs.append(limit)
    # score = linter.stats['global_note']
    score = linter.stats.global_note

    print(f"pylint score = {score} limit = {limit}")
    assert score >= limit


@pytest.fixture(
    name="input_image",
    params=[p for p in (Path(__file__).parent / 'test_images').iterdir() if p.suffix != '.sign']
)
def _input_image(request):
    img = cv2.imread(str(request.param))
    return request.param.stem, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


@pytest.mark.parametrize(
    "n_pyr_layers,downscale_factor", [[1, 1.0], [2, 4.0], [3, 2.0], [5, 1.2]]
)
def test_create_pyramid(input_image, n_pyr_layers, downscale_factor):
    _, img0 = input_image
    pyr = orb.create_pyramid(img0, n_pyr_layers, downscale_factor)
    assert isinstance(pyr, list)
    assert all(isinstance(img_level, np.ndarray) for img_level in pyr)
    assert len(pyr) == n_pyr_layers
    assert np.array_equal(pyr[0], img0)
    img = img0.copy()
    for i in range(1, n_pyr_layers):
        out_shape = tuple(math.ceil(d / float(downscale_factor)) for d in img.shape)
        pixels_total = out_shape[0] * out_shape[1]
        assert abs(out_shape[0] - pyr[i].shape[0]) <= 2
        assert abs(out_shape[1] - pyr[i].shape[1]) <= 2
        img = cv2.resize(img, pyr[i].shape[::-1])
        pixels_ok = np.isclose(
            img.astype(np.uint8), 
            pyr[i].astype(np.uint8), 
            atol=5
        ).sum()
        if (pixels_ok / pixels_total) < 0.9:
            img = cv2.resize(img0, pyr[i].shape[::-1])
            pixels_ok = np.isclose(
                img.astype(np.uint8), 
                pyr[i].astype(np.uint8), 
                atol=5
            ).sum()
        assert (pixels_ok / pixels_total) >= 0.9


@pytest.mark.parametrize(
    "threshold,border", [[5, 0], [5, 10], [10, 0], [10, 20], [20, 0], [20, 20]]
)
def test_get_first_test_mask(input_image, threshold, border):
    _, img = input_image
    border = max(border, orb.FAST_CIRCLE_RADIUS)
    mask = orb.get_first_test_mask(img.astype(int), threshold, border)
    assert isinstance(mask, np.ndarray)
    assert mask.shape == img.shape
    assert mask[:border, :].sum() == 0
    assert mask[:, :border].sum() == 0
    assert mask[-border:, :].sum() == 0
    assert mask[:, -border:].sum() == 0


@pytest.mark.parametrize(
    "threshold,border", [[30, 50],[20, 20]]
)
def test_calculate_kp_scores(input_image, threshold, border):
    img = input_image[1].astype(int)
    border = max(border, orb.FAST_CIRCLE_RADIUS)
    keypoints, scores = orb.detect_keypoints(img, threshold, border)
    assert isinstance(scores, list)
    assert all([isinstance(score, int) for score in scores])


@pytest.mark.parametrize(
    "threshold,border", [[5, 20], [20, 20]]
)
def test_detect_keypoints(input_image, threshold, border):
    keypoints, _ = orb.detect_keypoints(input_image[1], threshold, border)
    assert isinstance(keypoints, list)


def test_get_x_derivative(input_image):
    result = orb.get_x_derivative(input_image[1])
    assert input_image[1].shape == result.shape


def test_get_y_derivative(input_image):
    result = orb.get_x_derivative(input_image[1])
    assert input_image[1].shape == result.shape


@pytest.mark.parametrize(
    "n_max,threshold,border",
    [
        [50, 20, 0],
        [100, 15, 10],
        [150, 10, 0],
        [250, 20, 10],
    ],
)
def test_filter_keypoints(input_image, n_max, threshold, border):
    keypoints, _ = orb.detect_keypoints(input_image[1], threshold, border=border)
    filtered_keypoints = orb.filter_keypoints(input_image[1], keypoints, n_max)
    assert len(filtered_keypoints) <= n_max
