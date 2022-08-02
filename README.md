# Endoscopic Content Area (ECA) dataset
A simple python loader for the [Endoscopic Content Area (ECA) dataset](https://doi.org/10.7303/syn32148000). An implementation of the [hausdorff distance](https://en.wikipedia.org/wiki/Hausdorff_distance), optimised for content areas, is also included in the package.

[![Build Status](https://github.com/charliebudd/eca-dataset/actions/workflows/release.yml/badge.svg)](https://github.com/charliebudd/eca-dataset/actions/workflows/release.yml)

## Installation
To use this dataset, first ensure you have a synapse account, then simply install from pip...
```bash
pip install ecadataset
```
and run the download command...
```bash
download-eca -d path/to/dataset
```
You'll be prompted for your synapse credentials and the data will be downloaded.

## Usage

```python
import matplotlib.pyplot as plt
from eca import ECADataset, DataSource, AnnotationType, content_area_hausdorff

# Create dataset object...
dataset = ECADataset(
  # Path to the directory containing the dataset.
  data_directory="path/to/dataset",
  # Options are: DataSource.CHOLEC, DataSource.ROBUST, and DataSource.BOTH.
  data_source=DataSource.BOTH,
  # Options are: AnnotationType.AREA, AnnotationType.MASK, and AnnotationType.BOTH.
  annotation_type=AnnotationType.BOTH,
  # Whether to use cropping to provide additonal samples without a content area.
  include_cropped=True,
  # Whether to include information about where the frame was taken from.
  include_source_info=True
)

# Iterate through the first 10 samples, slicing is supported...
for image, area, mask, info in dataset[:10]:

    # Circular content area represented as (x, y, r) or None if no area present...
    print("Content area: ", area)
    
    # Origin information in the form (dataset, video, frame)...
    print("Sample source: ", info)
    
    # Image and mask are returned as PIL images...
    plt.subplot(121)
    plt.imshow(image)
    plt.subplot(122)
    plt.imshow(mask)
    plt.show()
    
    # Guessing the content area circle and scoring it against the ground truth...
    width, height = image.size
    area_guess = (width//2, height//2, width//2)
    score, _ = content_area_hausdorff(area_guess, area, (height, width))
    print(score)
```

