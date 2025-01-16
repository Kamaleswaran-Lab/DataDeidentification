import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

from emrd import *

hash_key = '123'
#YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

if __name__ == "__main__":

    path_to_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/')
    path_to_deid_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/anon')

    #parser = ArgumentParser()
    #parser.add_argument('--index', type = int, required = True)
    #args = parser.parse_args()
    #year = YEARS[args.index]
    #print(year)
    
    path_to_data = path_to_data #/ str(year)
    path_to_deid_data = path_to_deid_data #/ str(year)
    path_to_deid_data.mkdir(parents = True, exist_ok = True)
  
    settings = {
    #'Metadata': EMRDeidentification(file_name= path_to_data / 'metadata.csv' , deid_path= path_to_deid_data,
    #                                 type = 'Meta',  
    #                                 hash_columns = ['PatientID', 'StudyInstanceUID', 'SeriesInstanceUID', 'SOPInstanceUID', 'AccessionNumber'], 
    #                                 drop_columns = [], age_columns= [],
    #                                 categorical_columns = [], 
    #                                 date_columns = [], 
    #                                 hash_key = hash_key, sep = ','),
    #'Metadata_with_Encounter': EMRDeidentification(file_name= path_to_data / 'metadata_with_encounter_matched.csv' , deid_path= path_to_deid_data,
    #                                 type = 'Meta',  
    #                                 hash_columns = [ 'ENCOUNTER_NBR', 'PatientID', 'PAT_ID', 'ENCOUNTER_ID', 'AccessionNumber'], 
    #                                 drop_columns = [], age_columns= [],
    #                                 categorical_columns = [], 
    #                                 date_columns = [], 
    #                                 hash_key = hash_key, sep = ','),
    #'Metadata_with_Supertables': EMRDeidentification(file_name= path_to_data / 'metadata_with_supertables.pickle' , deid_path= path_to_deid_data,
    #                                 type = 'Meta',  
    #                                 hash_columns = ['EMPI_NBR', 'ENCOUNTER_NBR', 'PatientID', 'PAT_ID', 'ENCOUNTER_ID', 'AccessionNumber'], 
    #                                 drop_columns = [],  age_columns= [],
    #                                 categorical_columns = [], 
    #                                 date_columns = [], 
    #                                 hash_key = hash_key, sep = ','),
    #'Ventilator': EMRDeidentification(file_name= path_to_data / f'vent_o2_flow_rate{year}.csv' , deid_path= path_to_deid_data,
    #                                    type = 'Ventilator',
    #                                    hash_columns = ['PATIENT_ID', 'EMPI_NBR', 'ENCOUNTER_ID', 'ENCOUNTER_NBR'],
    #                                    drop_columns = [], age_columns= [],
    #                                    categorical_columns = [],
    #                                    date_columns = [],
    #                                    hash_key = hash_key, sep = ','),
    'Notes15': EMRDeidentification(file_name= path_to_data /'IBJG_CXR_ACC_15_20.csv',  deid_path= path_to_deid_data,
                                    type = 'Notes',
                                    hash_columns = ['ACC_NBR', 'PATIENT_ID', 'EMPI_NBR', 'ENCNTR_ID', 'EVENT_DOCUMENT_DESC', \
                                                    'HNAM_DOCUMENT_CLINICAL_ID', 'ENCOUNTER_ID', 'ENCOUNTER_NBR'],
                                    drop_columns = [], age_columns= [],
                                    categorical_columns = [],
                                    date_columns = ['DAY_VERIFIED'],
                                    hash_key = hash_key, sep = ','),
    'Notes21': EMRDeidentification(file_name= path_to_data /'IBJG_CXR_ACC_21_22.csv',  deid_path= path_to_deid_data,
                                    type = 'Notes',
                                    hash_columns = ['ACC_NBR', 'PATIENT_ID', 'EMPI_NBR', 'ENCNTR_ID', 'EVENT_DOCUMENT_DESC', \
                                                    'HNAM_DOCUMENT_CLINICAL_ID', 'ENCOUNTER_ID', 'ENCOUNTER_NBR'],
                                    drop_columns = [], age_columns= [],
                                    categorical_columns = [],
                                    date_columns = ['DAY_VERIFIED'],
                                    hash_key = hash_key, sep = ','),

                                     }
    for key in settings:
        print(key)
        settings[key].read_file()
        if key.startswith('Notes'):
            settings[key].hash_identifiers(save = True)
        else:
            settings[key].hash_identifiers()
        settings[key].hash_identifiers(save = True)
        settings[key].drop_identifiers()
        settings[key].convert_to_categorical()
        settings[key].shift_dates()
        settings[key].save_file()