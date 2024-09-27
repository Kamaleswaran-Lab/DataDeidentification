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
    path_to_combined_meta = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta_' + year + '_MRN.csv')
    combined_meta = pd.read_csv(path_to_combined_meta)

    path_to_mastertable = Path('/labs/kamaleswaranlab/MODS/Data/Emory_Data/RKENCOUNTERS_BEDLOCATION.csv')
    mastertable = pd.read_csv(path_to_mastertable)

    date_columns = ['ContentDate', 'PresentationCreationDate', 'SeriesDate', 'StudyDate', 'AcquisitionDate', 'InstanceCreationDate']
    #Convert date columns to datetime
    for col in date_columns:
        combined_meta[col + '_datetime'] = pd.to_datetime(combined_meta[col], errors='coerce')
    
    combined_meta['ENCOUNTER_NBR'] = np.nan
    combined_meta['ENCOUNTER_ID'] = np.nan
    mastertable['BED_LOCATION_START'] = pd.to_datetime(mastertable['BED_LOCATION_START'])
    mastertable['BED_LOCATION_END'] = pd.to_datetime(mastertable['BED_LOCATION_END'])
    
    print("Matching...")
    import pdb; pdb.set_trace()
    for idx, row in combined_meta.iterrows():
        #Match on Patient ID and date 
        patient_id = row['PAT_ID']
        for date in date_columns:
            if not pd.isnull(row[date + '_datetime']):
                date = row[date + '_datetime']
                break
            else:
                date = np.nan
        
        if pd.isnull(date):
            combined_meta.at[idx, 'ENCOUNTER_NBR'] = np.nan
            combined_meta.at[idx, 'ENCOUNTER_ID'] = np.nan
            break

        else: 
            mastertable_match = mastertable[(mastertable['PAT_ID'] == patient_id) & (mastertable['BED_LOCATION_START'] <= date) & (mastertable['BED_LOCATION_END'] >= date)]
            if len(mastertable_match) > 0:
                combined_meta.at[idx, 'ENCOUNTER_NBR'] = mastertable_match['ENCOUNTER_NBR'].values[0]
                combined_meta.at[idx, 'ENCOUNTER_ID'] = mastertable_match['ENCOUNTER_ID'].values[0]
            else:
                combined_meta.at[idx, 'ENCOUNTER_NBR'] = np.nan
                combined_meta.at[idx, 'ENCOUNTER_ID'] = np.nan
    
    combined_meta.to_csv(path_to_combined_meta, index=False)
    print("Done")
