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
    path_to_combined_meta = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '.pkl')
    combined_meta = pd.read_pickle(path_to_combined_meta)
    
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
    
    path_all_empi = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/all_empi_' + year + '.csv')
    all_empi = pd.read_csv(path_all_empi)

    #Match on Patient ID and date 
    combined_meta['PatientID'] = combined_meta['PatientID'].astype(int)
    patient_ids = combined_meta['PatientID'].unique()
    print("Number of unique patients: ", len(patient_ids))

    combined_meta['true_empi'] = combined_meta['PatientID'].apply(lambda x: all_empi.iloc[x]['PatientID'] if x in all_empi.index else np.nan)
    #Join combined_meta with mastertable on true_empi and EMPI_NBR
    mastertable_subset = mastertable[['PAT_ID', 'EMPI_NBR']]
    mastertable_subset = mastertable_subset.drop_duplicates()
    combined_meta = combined_meta.merge(mastertable_subset, left_on = 'true_empi', right_on = 'EMPI_NBR', how = 'left')

    #Check for missing values
    print("Number of missing values in MRN: ", combined_meta['PAT_ID'].isnull().sum())
    print("Number of missing values in PatientID: ", combined_meta['PatientID'].isnull().sum()) 

    combined_meta.to_csv('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_MRN.csv', index = False)
    print("Updated meta data saved to: ", '/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_MRN.csv')
    
    """
    
    for i, patient_id in enumerate(patient_ids):
        true_empi = all_empi.iloc[int(patient_id)]['PatientID']
        empi_match = mastertable.loc[mastertable['EMPI_NBR'] == true_empi]
        if len(empi_match) == 0:
            print("No match found for patient: ", patient_id)
            #Write to file
            with open('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/No_Match_' + year + '.txt', 'a') as f:
                f.write(str(patient_id) + '\n')
            continue
        else:
            print("Match found for patient: ", patient_id)    
            combined_meta.loc[combined_meta['PatientID'] == patient_id, 'MRN_PatientID'] = empi_match['PAT_ID'].values[0]
    
    #Save the updated meta data
    combined_meta.to_csv('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_MRN.csv', index = False)
    print("Updated meta data saved to: ", '/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_MRN.csv')

    """