from .dataset import ECADataset, DataSource, AnnotationType
from .scoring import content_area_hausdorff
from . import _version
__version__ = _version.get_versions()['version']
