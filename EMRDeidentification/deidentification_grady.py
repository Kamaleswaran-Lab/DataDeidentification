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
    year = args.index
    print(year)

    path_to_data = Path('/labs/collab/K-lab-MODS/MODS-PHI/Grady_Data/')
    path_to_deid_data = Path('/labs/collab/K-lab-MODS/deid_grady/noPHI')

    path_to_data = path_to_data 
    path_to_deid_data = path_to_deid_data / str(year) #'decomp_by_MRN'
    path_to_deid_data.mkdir(parents = True, exist_ok = True)


    settings = {
        """
    'Encounter': EMRDeidentification(file_name= path_to_data / '1. Administrative Attributes/Encounters'/ f'encounter_2014-2022_decomp*.txt' , deid_path= path_to_deid_data,
                                     type = 'Encounter',  
                                     hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     age_columns = ['age'],
                                     date_columns = ['ed_presentation_time', 'hospital_admission_date_time', \
                                                     'hospital_discharge_date_time'], 
                                     hash_key = hash_key),
    'BedLocation': EMRDeidentification(file_name= path_to_data / '1. Administrative Attributes/Bed Locations' /f'bed_location_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'BedLocation', 
                                     hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                     drop_columns = [], 
                                     categorical_columns = [], 
                                     age_columns= [],
                                     date_columns = ['bed_location_start', 'bed_location_end'], 
                                     hash_key = hash_key),
    'Diagnosis': EMRDeidentification(file_name= path_to_data /'5. ICD Codes/Diagnosis' / f'diagnoses_2014-2022_decomp*.txt',  deid_path= path_to_deid_data, 
                                    type = 'Diagnosis',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['dx_time_date'], 
                                    age_columns= [],
                                    hash_key = hash_key),
    'Demographics': EMRDeidentification(file_name= path_to_data / '1. Administrative Attributes/Demographics'/ f'demographics_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'Demographics',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['first_name', 'last_name', 'mi', 'last4_ssn', 'dob', 'death_date', 'race', 'ethnicity'],
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = [], 
                                    hash_key = hash_key),
    'Cultures': EMRDeidentification(file_name= path_to_data / '3. Labs & Cultures/Cultures' / f'cultures_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'Cultures',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['order_id', 'result_id'], 
                                    categorical_columns = [], 
                                    date_columns = ['specimen_collect_time', 'order_time', 'lab_result_time'], 
                                    age_columns= [],
                                    hash_key = hash_key),
    #'Labs': EMRDeidentification(file_name= path_to_data /'3. Labs & Cultures/Labs' / f'lab_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
    #                                type = 'Labs',
    #                                hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
    #                                drop_columns = [], 
    #                                categorical_columns = [], 
    #                                age_columns= [],
    #                                date_columns = ['collection_time', 'lab_result_time'], 
    #                                hash_key = hash_key),
    'Vitals': EMRDeidentification(file_name= path_to_data /'4. Patient Assessments/Vitals'/ f'vitals_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'Vitals',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['recorded_time'], 
                                    hash_key = hash_key),
    'GCS': EMRDeidentification(file_name= path_to_data /'4. Patient Assessments/GCS'/ f'gcs_2014-2022_decomp*.txt',  deid_path= path_to_deid_data, 
                                    type = 'GCS',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['recorded_time'], 
                                    hash_key = hash_key),
    'INFUSIONMEDS': EMRDeidentification(file_name= path_to_data /'2. Fluids & Meds/Infusion Medications' / f'infusion_meds_2014-2022_decomp_*.txt',  deid_path= path_to_deid_data,
                                    type = 'INFUSIONMEDS',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['order_med_id'], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['med_order_time', 'med_action_time', 'med_start', 'med_stop'], 
                                    hash_key = hash_key),
    'NONINFUSIONMEDS': EMRDeidentification(file_name= path_to_data /'2. Fluids & Meds/Non-Infusion Medications' / f'non_infusion_meds_2014-2022_decomp_*.txt',  deid_path= path_to_deid_data,
                                    type = 'NONINFUSIONMEDS',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['order_med_id'], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['med_order_time', 'med_action_time', 'med_start', 'med_stop'], 
                                    hash_key = hash_key),
    'ICDPROCEDURE': EMRDeidentification(file_name= path_to_data /'5. ICD Codes/ICD Procedures' / f'icd_procedures_2014-2022_decomp*.txt' ,  deid_path= path_to_deid_data,
                                     type = 'ICDPROCEDURE',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['performing_physician'], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = [ 'procedure_date'], 
                                    hash_key = hash_key),
    'ORPROCEDURE': EMRDeidentification(file_name= path_to_data /'5. ICD Codes/OR Procedures' / f'or_procedures_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'ORPROCEDURE',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['log_id', 'primary_physician_nm'], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['surgery_date', 'in_or_dttm', 'procedure_start_dttm', 'procedure_comp_dttm', 'out_or_dttm'], 
                                    hash_key = hash_key),
    'SENSITIVITIES': EMRDeidentification(file_name= path_to_data / '3. Labs & Cultures/Sensitivities' / f'sensitivities_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                     type = 'SENSITIVITIES',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = ['order_id', 'result_id'], 
                                    categorical_columns = [], 
                                    age_columns= [],
                                    date_columns = ['order_time', 'sens_obs_inst_tm', 'sens_anl_inst_tm'], 
                                    hash_key = hash_key),
    'VENT': EMRDeidentification(file_name= path_to_data /'6. Vent'/ f'vent*_2014-2022_*.txt',  deid_path= path_to_deid_data,
                                    type = 'VENT',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    age_columns= [],
                                    categorical_columns = [], 
                                    date_columns = ['recorded_time', 'vent_start_time', 'vent_stop_time', 'vent_recorded_time'], 
                                    hash_key = hash_key),
    'RADIOLOGY': EMRDeidentification(file_name= path_to_data /'7. Radiology'/ f'radiology*_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'RADIOLOGY',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id', 'accession_num'], 
                                    drop_columns = ['order_id'], 
                                    categorical_columns = [], 
                                    date_columns = ['rad_order_time', 'begin_exam_dttm', 'end_exam_dttm'], 
                                    age_columns = [],
                                    hash_key = hash_key),
    'LINES': EMRDeidentification(file_name= path_to_data /'8. Lines'/ 'Central Line' / f'central_line_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'LINES',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['placement_date', 'removal_date'], 
                                    age_columns = [],
                                    hash_key = hash_key),
    'COMORBIDITIES': EMRDeidentification(file_name= path_to_data /'4. Patient Assessments/Comorbidities'/ f'comorbidities*_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'COMORBIDITIES',
                                    hash_columns = ['PAT_MRN_ID'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['DATE_OF_ENTRY'], 
                                    age_columns = [],
                                    hash_key = hash_key),
    'FAST': EMRDeidentification(file_name= path_to_data /'4. Patient Assessments/FAST'/ f'fast_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
                                    type = 'FAST',
                                    hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                    drop_columns = [], 
                                    categorical_columns = [], 
                                    date_columns = ['recorded_time'], 
                                    age_columns = [],
                                    hash_key = hash_key), """
    'BLOODTRANSFUSIONS': EMRDeidentification(file_name= path_to_data /'2. Fluids & Meds/Blood Products'/ f'blood_transfusion*_{year}_decomp*.txt',  deid_path= path_to_deid_data,
                                type = 'BLOODTRANSFUSIONS',
                                hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
                                drop_columns = ['order_id'], 
                                categorical_columns = [], 
                                date_columns = ['documented_time', 'order_time', 'transfusion_start', 'transfusion_end', 'transfusion_complete_time'], 
                                age_columns = [],
                                hash_key = hash_key),
    #'INOUT': EMRDeidentification(file_name= path_to_data /'2. Fluids & Meds/In\'s & Out\'s'/ f'intake_output_2014-2022_decomp*.txt',  deid_path= path_to_deid_data,
    #                            type = 'INOUT',
    #                            hash_columns = ['pat_id', 'csn', 'har', 'mrn', 'study_id'], 
    #                            drop_columns = [], 
    #                            categorical_columns = [], 
    #                            date_columns = ['documented_time'], 
    #                            age_columns = [],
    #                            hash_key = hash_key),
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

    
