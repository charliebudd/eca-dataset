import synapseclient
import synapseutils
from os import path, devnull
from getpass import getpass
from enum import Flag, auto
from json import load
from math import sqrt, floor
from PIL import Image
from contextlib import redirect_stdout

class DataSource(Flag):
    CHOLEC = auto()
    ROBUST = auto()
    BOTH = CHOLEC | ROBUST

class AnnotationType(Flag):
    AREA = auto()
    MASK = auto()
    BOTH = AREA | MASK

class ECADataset():
    def __init__(self, data_directory="eca-data", data_source=DataSource.BOTH, annotation_type=AnnotationType.AREA, include_cropped=True, include_source_info=False) -> None:
        super().__init__()
        self.data_directory = data_directory
        self.annotation_type = annotation_type
        self.data_source = data_source
        self.include_cropped = include_cropped
        self.include_source_info = include_source_info

        self.sample_list = []
        if DataSource.CHOLEC in self.data_source:
            self.sample_list += get_sample_list(data_directory, DataSource.CHOLEC)
        if DataSource.ROBUST in self.data_source:
            self.sample_list += get_sample_list(data_directory, DataSource.ROBUST)

        if self.include_cropped:
            self.sample_list = add_cropped_samples(self.data_directory, self.sample_list)

    def __len__(self):
        return len(self.sample_list)

    def __getitem__(self, key):

        if isinstance(key, slice):
            indices =  range(*key.indices(len(self)))
            return (self[i] for i in indices)
            
        sample = self.sample_list[key]
        
        frame = Image.open(path.join(self.data_directory, sample['image_file']))
        if self.include_cropped and sample['crop'] != None:
            frame = frame.crop(sample['crop'])
        result = (frame,)

        if AnnotationType.AREA in self.annotation_type:
            result = (*result, sample['content_area'])

        if AnnotationType.MASK in self.annotation_type:
            mask = Image.open(path.join(self.data_directory, sample['mask_file']))
            if self.include_cropped and sample['crop'] != None:
                mask = mask.crop(sample['crop'])
            result = (*result, mask)

        if self.include_source_info:
            result = (*result, sample['source_info'])

        return result

# ========================================
# Some helper methods...

syn = None

dataset_info = {
    DataSource.CHOLEC: {"name": "cholec-eca", "pretty_name": "CholecECA", "synapse_id": "syn32150390"},
    DataSource.ROBUST: {"name": "robust-eca", "pretty_name": "RobustECA", "synapse_id": "syn32150393"}
}

def get_synapse_session(data_directory):
    global syn
    if syn == None:
        syn = synapseclient.Synapse()
        print("Some of the requested data cannot be found at path \"" + path.abspath(data_directory) + "\"...\n")
        print("Please provide the correct path to the dataset, or provide your synapse credentials to download the dataset...")
        username = input("Synapse username:")
        password = getpass("Synapse password:")
        syn.login(username, password)
    return syn

def get_sample_list(data_directory, dataset_source):
    info = dataset_info[dataset_source]
    dataset_path = path.join(data_directory, info['name'])
    if not path.exists(dataset_path):
        syn = get_synapse_session(data_directory)
        print("Downloading " + info['pretty_name'] + " to " + dataset_path + "...")
        with redirect_stdout(open(devnull, 'w')):
            synapseutils.syncFromSynapse(syn, info['synapse_id'], path=dataset_path, manifest="suppress")
        print("Download finished.\n")
    with open(path.join(dataset_path, "manifest.json")) as file:
        return load(file)

def calculate_optimal_crop(circle, rectangle):

    r_w, r_h = rectangle
    c_x, c_y, c_r = circle

    aspect_ratio = r_w / r_h

    inscribed_height = 2 * (c_r - 2) / sqrt(1 + aspect_ratio * aspect_ratio)
    inscribed_width = inscribed_height * aspect_ratio

    left = max(c_x - inscribed_width / 2, 0)
    right = min(c_x + inscribed_width / 2, r_w)
    top = max(c_y - inscribed_height / 2, 0)
    bottom = min(c_y + inscribed_height / 2, r_h)

    x_scale = (right - left)
    y_scale = (bottom - top) * aspect_ratio

    scale = min(x_scale, y_scale)

    w = int(floor(scale))
    h = int(floor(scale / aspect_ratio))
    
    x = int(left + (right - left) / 2 - w / 2)
    y = int(top + (bottom - top) / 2 - h / 2)

    return x, y, x+w, y+h

def add_cropped_samples(data_directory, samples):
    new_samples = []
    for sample in samples:
        sample['crop'] = None
        new_samples.append(sample.copy())
        if sample['content_area'] != None:
            image_size = Image.open(path.join(data_directory, sample['mask_file'])).size
            sample['crop'] = calculate_optimal_crop(sample['content_area'], image_size)
            sample['content_area'] = None
            new_samples.append(sample)
    return new_samples
