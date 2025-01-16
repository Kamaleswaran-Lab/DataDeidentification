import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

from emrd import *

hash_key = '123'

if __name__ == "__main__":

    path_to_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays')
    path_to_deid_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/anon')

    path_to_data = path_to_data 
    path_to_deid_data = path_to_deid_data 
    path_to_deid_data.mkdir(parents = True, exist_ok = True)

  
    settings = {
    'Meta': EMRDeidentification(file_name= path_to_data / 'chest_xrays_new2015.csv' , deid_path= path_to_deid_data,
                                     type = 'Meta',  
                                     hash_columns = ['PatientID', 'PATIENTID', 'ENCNTR_ID', 'EMPI', 'StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'AccessionNumber'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     date_columns = ['AcquisitionDate'], 
                                     hash_key = hash_key, sep = ','),
    'Notes': EMRDeidentification(file_name= path_to_data /'Combined_Radiology_Notes_with_EncounterNumber.csv',  deid_path= path_to_deid_data,
                                    type = 'Notes', 
                                     hash_columns = ['ACC_NBR', 'PATIENT_ID', 'EMPI_NBR', 'ENCNTR_ID', 'EVENT_DOCUMENT_DESC', \
                                                     'HNAM_DOCUMENT_CLINICAL_ID', 'ENCOUNTER_ID', 'ENCOUNTER_NBR'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     date_columns = ['DAY_VERIFIED'], 
                                     hash_key = hash_key, sep = ','),
                                     
                                     }
    for key in settings:
        print(key)
        settings[key].read_file()
        if key == 'Encounter':
            settings[key].hash_identifiers(save = True)
        else:
            settings[key].hash_identifiers()
        settings[key].drop_identifiers()
        settings[key].convert_to_categorical()
        settings[key].shift_dates()
        settings[key].save_file()