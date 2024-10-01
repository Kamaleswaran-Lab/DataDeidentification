import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

from emrd import *

YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
hash_key = '123'

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--index', type = int, required = True)
    args = parser.parse_args()
    year = YEARS[args.index]
    print(year)

    path_to_data = Path('/labs/collab/K-lab-MODS/MODS-PHI/Emory_Data/')
    path_to_deid_data = Path('/labs/collab/K-lab-MODS/deid_Emory/noPHI')

    path_to_data = path_to_data / str(year)
    path_to_deid_data = path_to_deid_data / str(year)
    path_to_deid_data.mkdir(parents = True, exist_ok = True)


    settings = {
    'Encounter': EMRDeidentification(file_name= path_to_data / f'CJSEPSIS_ENCOUNTER_{year}.dsv' , deid_path= path_to_deid_data,
                                     type = 'Encounter',  
                                     hash_columns = ['pat_id', 'csn'], 
                                     drop_columns = ['zip_code'], 
                                     categorical_columns = ['facility_nm'], 
                                     date_columns = ['ed_presentation_time', 'hospital_admission_date_time', \
                                                     'hospital_discharge_date_time'], 
                                     hash_key = hash_key),
    'BedLocation': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_BEDLOCATION_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'BedLocation', 
                                     hash_columns = ['pat_id', 'csn'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     date_columns = ['bed_location_start', 'bed_location_end'], 
                                     hash_key = hash_key),
    'CPT': EMRDeidentification(file_name=path_to_data / f'CJSEPSIS_CPT_{year}.dsv',  deid_path= path_to_deid_data, type = 'CPT', 
                                     hash_columns = ['pat_id', 'csn'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     date_columns = ['procedure_dttm', 'procedure_day'], 
                                     hash_key = hash_key),
    'Diagnosis': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_DIAGNOSIS_{year}.dsv',  deid_path= path_to_deid_data, 
                                    type = 'Diagnosis',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['dx_time_date'], 
                                    hash_key = hash_key),
    'Demographics': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_DEMOGRAPHICS_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'Demographics',
                                    hash_columns = ['pat_id'], 
                                    drop_columns = ['first_name', 'last_name', 'mi', 'last4_ssn', 'dob', 'death_date', 'race', 'ethnicity'],
                                    categorical_columns = [], 
                                    date_columns = [], 
                                    hash_key = hash_key),
    'Cultures': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_CULTURES_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'Cultures',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['specimen_collect_time', 'order_time', 'lab_result_time'], 
                                    hash_key = hash_key),
    'Labs': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_LABS_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'Labs',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['collection_time', 'lab_result_time'], 
                                    hash_key = hash_key),
    'Vitals': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_VITALS_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'Vitals',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['recorded_time'], 
                                    hash_key = hash_key),
    'GCS': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_GCS_{year}.dsv',  deid_path= path_to_deid_data, 
                                    type = 'GCS',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = ['flo_row_id', 'flo_name'], 
                                    categorical_columns = [], 
                                    date_columns = ['recorded_time'], 
                                    hash_key = hash_key),
    'INFUSIONMEDS': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_INFUSIONMEDS_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'INFUSIONMEDS',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['med_order_time', 'med_action_time', 'med_start', 'med_stop'], 
                                    hash_key = hash_key),
    'NONINFUSIONMEDS': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_NONINFUSEDMEDS_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'NONINFUSIONMEDS',
                                    hash_columns = ['har', 'csn', 'patid'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['med_order_time', 'med_action_time', 'med_start_timestamp', 'med_stop_timestamp'], 
                                    hash_key = hash_key),
    'ICDPROCEDURE': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_ICDPROCEDURES_{year}.dsv',  deid_path= path_to_deid_data,
                                     type = 'ICDPROCEDURE',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = ['performing_physician'], 
                                    categorical_columns = [], 
                                    date_columns = [ 'procedure_date'], 
                                    hash_key = hash_key),
    'ORPROCEDURE': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_ORPROCEDURES_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'ORPROCEDURE',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['surgery_date', 'in_or_dttm', 'procedure_start_dttm', 'procedure_comp_dttm', 'out_or_dttm'], 
                                    hash_key = hash_key),
    'SENSITIVITIES': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_SENSITIVITIES_{year}.dsv',  deid_path= path_to_deid_data,
                                     type = 'SENSITIVITIES',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['order_time'], 
                                    hash_key = hash_key),
    'VENT': EMRDeidentification(file_name= path_to_data /f'CJSEPSIS_VENT_{year}.dsv',  deid_path= path_to_deid_data,
                                    type = 'VENT',
                                    hash_columns = ['pat_id', 'csn'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['recorded_time', 'vent_start_time', 'vent_stop_time'], 
                                    hash_key = hash_key)
    } 
    
    #import pdb; pdb.set_trace()
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

    
