import pandas as pd
import os
from pathlib import Path
#from multiprocessing import Pool, Lock
#import pydicom
import glob
import random
import string
import numpy as np
import pickle
import time
import sys
import hashlib

def hash_value(value, hash_key):
    return hashlib.sha256((str(value) + hash_key).encode()).hexdigest()

if __name__ == "__main__":
    year = sys.argv[1]
    
    path_to_mastertable = Path('/labs/kamaleswaranlab/MODS/Data/Emory_Data/RKENCOUNTERS_BEDLOCATION.csv')
    all_meta_columns = ['AccessionNumber', 'ContentDate', 'ContentDescription', 'ContentLabel', 'ContentTime',\
                        'ImageHorizontalFlip', 'ImageRotation', 'InstanceNumber', 'IssuerOfPatientID', 'Manufacturer', \
                        'ManufacturerModelName', 'Modality', 'PatientID', 'PatientSex', 'PresentationCreationDate', \
                            'PresentationCreationTime', 'ReferringPhysicianName', 'RescaleIntercept', 'RescaleSlope',\
                            'SOPClassUID', 'SOPInstanceUID', 'SeriesDate', 'SeriesDescription', 'SeriesInstanceUID', \
                            'SeriesNumber', 'SeriesTime', 'SoftwareVersions', 'SpecificCharacterSet', 'StationName', \
                            'StudyDate', 'StudyInstanceUID', 'StudyTime', 'file', 'has_pix_array', 'category', \
                            'AcquisitionDate', 'AcquisitionDateTime', 'AcquisitionTime', 'BitsAllocated',\
                            'BitsStored', 'Columns', 'HighBit', 'ImageType', 'InstitutionName', 'LossyImageCompression',\
                        'PatientOrientation', 'PhotometricInterpretation', 'PixelRepresentation', 'ProcessingFunction',\
                        'Rows', 'SamplesPerPixel', 'StudyDescription', 'StudyID', 'AcquisitionNumber', 'ConvolutionKernel',\
                    'DataCollectionDiameter', 'DeviceSerialNumber', 'DistanceSourceToDetector', 'DistanceSourceToPatient', \
                        'Exposure', 'ExposureTime', 'ImageOrientationPatient', 'ImagePositionPatient', 'InstanceCreationDate',\
                    'InstanceCreationTime', 'RescaleType', 'RevolutionTime', 'RotationDirection', 'ScanOptions', 'SliceLocation', \
                        'SliceThickness', 'SpacingBetweenSlices', 'EMPI']

    columns_to_deid = ['AccessionNumber',  'InstanceNumber', 'IssuerOfPatientID', \
                        'PatientID','SOPClassUID', 'SOPInstanceUID', 'StudyInstanceUID',  'InstitutionName',  'EMPI']
    
    all_mastertable_columns = ['PAT_ID', 'EMPI_NBR', 'ENCOUNTER_NBR', 'ENCOUNTER_ID', 'BED_LOCATION_START', 'BED_LOCATION_END', 'BED_UNIT', 'BED_ROOM', 'BED_ID', 'BED_LABEL', 'HOSPITAL_SERVICE', 'ACCOMODATION_CODE', 'ACCOMODATION_DESCRIPTION']
    columns_to_read = ['PAT_ID', 'EMPI_NBR', 'ENCOUNTER_NBR', 'ENCOUNTER_ID', 'BED_LOCATION_START', 'BED_LOCATION_END']

    mastertable = pd.read_csv(path_to_mastertable, usecols=  columns_to_read)
    
    path_to_combined_meta = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '.pkl')
    combined_meta = pd.read_pickle(path_to_combined_meta)

    path_to_combined_radiology_notes = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Radiology_Notes.csv')
    radiology_notes = pd.read_csv(path_to_combined_radiology_notes)

    for idx, row in combined_meta.iterrows():
        accession_number = row['AccessionNumber']
        radiology_note = radiology_notes.loc[radiology_notes['AccessionNumber'] == accession_number]
        if len(radiology_note) == 0:
            print("No radiology note for accession number: ", accession_number)
            continue

        #Append radiology note columns to combined_meta
        for col in radiology_note.columns:
            combined_meta.at[idx, col] = radiology_note[col].values[0]
        
    path_to_combined_meta = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_Radiology.pkl')
    combined_meta.to_pickle(path_to_combined_meta)



