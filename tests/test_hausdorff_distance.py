import unittest
import warnings
from parameterized import parameterized
import surface_distance
import numpy as np

from eca import content_area_hausdorff

TEST_PARAMETERS = [
    (None, None, (270, 480)),
    (None, (135, 240, 200), (270, 480)),
    ((135, 240, 100), (135, 240, 200), (270, 480)),
    ((0, 240, 300), (50, 240, 200), (270, 480)),
]

def compute_baseline_distance(circle_a, circle_b, frame_size):
    def draw_mask(circle, frame_size):
        if circle == None:
            mask = np.ones(frame_size).astype(bool)
        else:
            yy, xx = np.mgrid[:frame_size[0], :frame_size[1]]
            dist = (xx - circle[0]) ** 2 + (yy - circle[1]) ** 2
            mask = dist < circle[2]**2
        return np.pad(mask, ((10, 10), (10, 10)))
    a = draw_mask(circle_a, frame_size)
    b = draw_mask(circle_b, frame_size)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        distances = surface_distance.compute_surface_distances(a, b, (1, 1))
    return max(max(distances['distances_gt_to_pred']), max(distances['distances_pred_to_gt']))

class TestHausdorffDistance(unittest.TestCase):

    @parameterized.expand(TEST_PARAMETERS)
    def test_hausdorff_distance(self, circle_a, circle_b, frame_size):
        baseline = compute_baseline_distance(circle_a, circle_b, frame_size)
        score, _ = content_area_hausdorff(circle_a, circle_b, frame_size, normalise=False)
        one_percent = score / 100
        self.assertAlmostEqual(score, baseline, delta=one_percent)
