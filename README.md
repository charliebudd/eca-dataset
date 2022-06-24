# Endoscopic Content Area (ECA) dataset
A simple python loader for the Endoscopic Content Area (ECA) dataset.

## Installation
To use this dataset, first ensure you have a synapse account and access to the [ECA dataset](https://www.synapse.org/ecadataset). 
Then simply install from pip...
```bash
pip install ecadataset
```
On first usage, you'll be prompted for your synapse credentials and the data will be downloaded.

## Usage

```python
import matplotlib.pyplot as plt
from eca import ECADataset, DataSource, AnnotationType

# Create dataset object...
dataset = ECADataset(
  data_directory="path-to-dataset",     # Path to the dataset directory. If not found the dataset will be downloaded.
  data_source=DataSource.BOTH,          # Options are: DataSource.CHOLEC, DataSource.ROBUST, and DataSource.BOTH.
  annotation_type=AnnotationType.BOTH,  # Options are: AnnotationType.AREA, AnnotationType.MASK, and AnnotationType.BOTH.
  include_cropped=True,                 # Whether to use cropping to provide additonal samples without a content area.
  include_source_info=True              # Whether to include information about where the frame was taken from.
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
```

