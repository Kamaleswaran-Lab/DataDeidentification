import pydicom
from pydicom import config
import pandas as pd
import argparse
from pydicom import config
import numpy as np
import json
import os
import hashlib
import glob
from tqdm import tqdm
import warnings
import sys

config.image_handler = 'pylibjpeg'
warnings.filterwarnings('ignore')



def deidentify_dicom(dicom, anon: list, hash: list, hash_key:str):

    '''
    Description: Deidentifies DICOM file.

    Parameters:
        dicom (pydicom.dataset.FileDataset): DICOM object.
        anon (list): Fields to anonymize.
        hash (list): Fields to hash.
        hash_key (str) = Key to be added to the value.
        
    Returns:
        (dict): Deidentified DICOM.
    '''

    for elem in dicom:

        name = elem.keyword
        value = elem.value
            
        # For nested elements
        if type(value) is pydicom.sequence.Sequence:
            for i, item in enumerate(value):
                value[i] = deidentify_dicom(item, anon, hash, hash_key)

        else:

            if name in anon:
                try:
                    elem.value = 'Anonymized'
                except:
                    elem.value = 0.0

            if name in hash:
                elem.value = hash_value(str(value), hash_key)

    return dicom



def patid_mapping(pat_ids: list, mapping_path: str, hash_key: str):

    '''
    Description: Hashes each unique id and saves mapping file.

    Parameters:
        pat_ids (list): List of unique pat_ids.
        mapping_path (str): Location of the file with the mappings.
        hash_key (str): Key for hashing.
    '''

    # Check if hash mapping file exists
    if os.path.exists(os.path.join(mapping_path, 'pat_id_mapping.json')):
        with open(os.path.join(mapping_path, 'pat_id_mapping.json'), 'r') as f:
            mapping_dict = json.load(f)
    else:
        mapping_dict = {}

    # Assign hashed values to unique ids
    unique_ids = set(pat_ids)
    unique_ids = [str(id) for id in unique_ids if str(id) not in list(mapping_dict.keys())]
    hashed_values = [hash_value(id, hash_key) for id in unique_ids]
    mapping_dict.update({str(id): value for id, value in zip(unique_ids, hashed_values)})

    # Save updated dictionary
    with open(os.path.join(mapping_path, 'pat_id_mapping.json'), 'w') as f:
        json.dump(mapping_dict, f, indent=4)



def hash_value(value, hash_key:str):

    '''
    Description: Generates hashed value for given input.

    Parameters:
        value: Value to be hashed.
        hash_key (str): Key to be added to the value.
        
    Returns:
        str: Hashed value.
    '''

    hashed_value = hashlib.sha256((str(value) + hash_key).encode()).hexdigest()
    
    return hashed_value



def parse_arguments():

    '''
    Description: Parses arguments.
    '''

    parser = argparse.ArgumentParser(description='Deidentify CXR file.')
    parser.add_argument('--root', type=str, required=True, help='Location of the data.')

    args = parser.parse_args()

    return args






if __name__ == '__main__':

    '''
    Run from the terminal: python deidentify_cxr.py --root /path/to/data
    '''

    args = parse_arguments()
    root = args.root

    # Define columns to deid
    anon = ['ReferringPhysicianName', 'OperatorsName', 'PatientName', 'OtherPatientIDs', 'PatientAge', 'StudyDate', 
            'SeriesDate', 'AcquisitionDate', 'ContentDate', 'StudyTime', 'SeriesTime', 'AcquisitionTime', 'AccessionNumber',
            'PatientBirthDate', 'PatientAge', 'PatientAddress', 'StudyArrivalDate', 'StudyArrivalTime', 
            'StudyCompletionDate', 'StudyCompletionTime', 'PerformedProcedureStepStartDate']
    hash = ['SOPInstanceUID', 'ReferencedSOPInstanceUID', 'PatientID', 'StudyInstanceUID', 'SeriesInstanceUID', 
            'StudyID', 'RequestedProcedureID']
    
    # Define hash_key
    hash_key = '123'

    # Read paths
    print('\nReading paths...\n')
    paths = pd.read_pickle(os.path.join(root, 'cxr_data', 'metadata', 'dicom_paths.pkl'))
    pat_ids = []

    # Deidentify CXR
    print('Deidentifying CXR...')
    for dicom_path in tqdm(paths['path'], ncols=70, unit='CXRs'):
            
        try:

            # Load DICOM
            dicom = pydicom.dcmread(dicom_path, force=True)
            pat_ids.append(dicom['PatientID'].value)
            deid_dicom = deidentify_dicom(dicom, anon, hash, hash_key)

            # Save deidentified CXR
            save_path = os.path.join(root, 'cxr_data_deid', dicom_path.split('/')[5], 
                            deid_dicom['PatientID'].value, deid_dicom['StudyInstanceUID'].value, 
                            deid_dicom['SeriesInstanceUID'].value, f'{deid_dicom['SOPInstanceUID'].value}.dcm')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            deid_dicom.save_as(save_path)

        except:
            print(f'\nDeidentification of {dicom_path} failed\n')

    # Update path_id mappings
    print('\nUpdating mappings...')
    patid_mapping(pat_ids, os.path.join(root, 'mappings'), hash_key)
    print('\nDone!\n')