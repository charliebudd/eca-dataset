import os
import unittest
from PIL import Image
from typing import Sequence

from eca import ECADataset, DataSource, AnnotationType

CHOLEC_SAMPLE_COUNT = 3929
ROBUST_SAMPLE_COUNT = 2994

class TestDataLoader(unittest.TestCase):

    def test_sample_counts(self):
        dataset = ECADataset(data_source=DataSource.CHOLEC)
        self.assertEqual(len(dataset), CHOLEC_SAMPLE_COUNT)
        dataset = ECADataset(data_source=DataSource.ROBUST)
        self.assertEqual(len(dataset), ROBUST_SAMPLE_COUNT)
        dataset = ECADataset(data_source=DataSource.BOTH)
        self.assertEqual(len(dataset), CHOLEC_SAMPLE_COUNT + ROBUST_SAMPLE_COUNT)

    def test_sample_loading(self):
        dataset = ECADataset(annotation_type=AnnotationType.BOTH, include_source_info=True)
        for image, area, mask, info in dataset[::250]:
            self.assertIsInstance(image, Image.Image)
            if area != None:
                self.assertIsInstance(area, Sequence)
                self.assertEqual(len(area), 3)
                self.assertIsInstance(area[0], int)
                self.assertIsInstance(area[1], int)
                self.assertIsInstance(area[2], int)
            self.assertIsInstance(mask, Image.Image)
            self.assertEqual(image.size, mask.size)
            self.assertIsInstance(info, Sequence)
            self.assertEqual(len(info), 3)
            self.assertIsInstance(info[0], str)
            self.assertIsInstance(info[1], str)
            self.assertIsInstance(info[2], int)

    def test_slicing(self):
        dataset = ECADataset(include_source_info=True)
        key = slice(10, 25, 5)
        indices = range(*key.indices(len(dataset)))
        subset = dataset[key]
        for sample, origin_index in zip(subset, indices):
            self.assertEqual(sample[2], dataset[origin_index][2])
