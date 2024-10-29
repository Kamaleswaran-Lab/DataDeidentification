import pydicom
from pydicom import config
import pandas as pd
import argparse
from pydicom import config
import numpy as np
import os
import glob
from tqdm import tqdm
import warnings
import sys

config.image_handler = 'pylibjpeg'
warnings.filterwarnings('ignore')



def get_metadata_dict(dicom, elem_subset: list, prefix: str=""):

    '''
    Description: Extracts metadata from DICOM file.

    Parameters:
        dicom (pydicom.dataset.FileDataset): DICOM object.
        prefix (str): Prefix for nested metadata.
        elem_subset (list): List of selected elements.
        
    Returns:
        (dict): Dictionary with all metadata name-value pairs.
    '''

    # Initialize dictionary
    metadata_dict = {}

    for elem in dicom:

        name = elem.keyword
        value = elem.value

        # Do not include image data
        if name != 'PixelData': 
            
            # For nested elements
            if type(value) is pydicom.sequence.Sequence:
                if len(value) == 0:
                    if f'{prefix}{name}' in elem_subset:
                        metadata_dict[f'{prefix}{name}'] = np.nan
                else:
                    for i, item in enumerate(value):
                        metadata_dict.update(get_metadata_dict(item, elem_subset, prefix=f'{prefix}{name}({i})_'))

            else:
                if f'{prefix}{name}' in elem_subset:
                    value = convert_value_type(value)
                    value = value if value != '' else np.nan
                    metadata_dict[f'{prefix}{name}'] = value

    return metadata_dict



def extract_metadata(dicom_paths: list, n_splits: int, year_idx: int, root: str):

    '''
    Description: Extracts metadata from multiple DICOM files and stores it in a pkl file.

    Parameters:
        dicom_paths (list): List of the DICOM files.
        n_splits (int): Number of splits of the DICOM files, i.e. generated metadata files.
        year_idx (int): Index of the year folder in the file path.
        root (str): Root of the folder of the DICOM files.
    '''

    # Get specific set of elements to extract
    try:
        elem_subset = open(os.path.join(root, 'metadata', 'feature_set.txt')).read().splitlines()
    except Exception as e:
        sys.exit(f'{e}')

    # Create splits of path files
    dicom_paths_splits = np.array_split(dicom_paths, n_splits)

    for i, dicom_paths_split in enumerate(dicom_paths_splits):

        # Initialize list
        all_metadata = []

        # Loop through DICOM files in split
        for path in tqdm(dicom_paths_split, ncols=70, desc=f'Split {i+1}/{n_splits}'):

            # Read file and extract metadata
            dicom = pydicom.dcmread(path, force=True)
            metadata = get_metadata_dict(dicom, elem_subset)

            # Add extra elements to metadata
            pix_array = True
            try:
                dicom.pixel_array
            except:
                pix_array = False
            metadata['PixArray'] = pix_array
            metadata['Folder'] = path.split('/')[year_idx]
            metadata['File'] = '/'.join(path.split('/')[year_idx:])

            all_metadata.append(metadata)

        # Save metadata
        print(f'Saving metadata file {i+1}...\n')
        metadata_df = pd.DataFrame(all_metadata)
        metadata_df.to_pickle(os.path.join(root, 'metadata', f'metadata_{i}.pkl'))



def merge_metadata(root: str):

    '''
    Description: Merges metadata files into a single file.

    Parameters:
        root (str): Root of the folder of the DICOM files.
    '''

    # Get list of metadata files
    metadata_files = [filename for filename in os.listdir(os.path.join(root, 'metadata')) if 'metadata' in filename]

    # Merge metadata files
    for i, filename in enumerate(metadata_files):

        if i == 0:
            metadata_df = pd.read_pickle(os.path.join(root, 'metadata', filename))
        else:
            metadata_df = pd.concat([metadata_df, pd.read_pickle(os.path.join(root, 'metadata', filename))], 
                                    axis=0, ignore_index=True)
    
    # Save merged file
    print('Saving metadata file...')
    metadata_df.to_pickle(os.path.join(root, 'metadata', 'metadata.pkl'))



def convert_value_type(value):

    '''
    Description: Converts pydicom-specific data type into standard Python data type.
    '''

    if type(value) is pydicom.valuerep.DSfloat:
        value = float(value)
    elif type(value) is pydicom.valuerep.IS:
        value = str(value)
    elif type(value) is pydicom.valuerep.PersonName:
        value = str(value)
    elif type(value) is pydicom.multival.MultiValue:
        value = tuple(value)
    elif type(value) is pydicom.uid.UID:
        value = str(value)

    return value



def get_paths(root: str, pattern: str='**/*.dcm'):

    '''
    Description: Creates file with paths that match the pattern.

    Parameters:
        root (str): Root of the path.
        pattern (str): Pattern to match.
        
    Returns:
        (list): List of paths.
    '''

    paths = glob.glob(os.path.join(root, pattern), recursive=True)
    paths_df = pd.DataFrame(paths, columns=['path'])
    os.makedirs(os.path.join(root, 'metadata'), exist_ok=True)
    paths_df.to_pickle(os.path.join(root, 'metadata', 'dicom_paths.pkl'))



def parse_arguments():

    '''
    Description: Parses arguments.
    '''

    parser = argparse.ArgumentParser(description='Extract metadata.')
    parser.add_argument('--root', type=str, required=True, help='Root of images path.')
    parser.add_argument('--n_splits', type=int, required=True, help='Number of splits of data.')
    parser.add_argument('--year_idx', type=int, required=True, help='Index of year folder in path.')
    parser.add_argument('--paths', action='store_true', help='Flag to create paths file.')

    args = parser.parse_args()

    return args




if __name__ == '__main__':

    '''
    Run from the terminal: python extract_metadata.py --root /path/to/root_directory --n_splits n --year_index i -- paths
    '''

    args = parse_arguments()
    root = args.root
    n_splits = args.n_splits
    year_idx = args.year_idx
    paths_flag = args.paths

    # Get paths
    print('\nGetting paths...')
    if paths_flag:
        get_paths(root)
    dicom_paths = pd.read_pickle(os.path.join(root, 'metadata', 'dicom_paths.pkl'))
    dicom_paths = dicom_paths['path']

    # Extract metadata
    print('Extracting metadata...\n')
    extract_metadata(dicom_paths, n_splits, year_idx, root)

    # Merge metadata
    print('Merging metadata...\n')
    merge_metadata(root)

    print('Done!\n')

