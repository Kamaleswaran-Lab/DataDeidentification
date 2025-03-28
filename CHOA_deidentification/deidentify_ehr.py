import pandas as pd
import numpy as np
import hashlib
import os
import argparse
import json
import warnings

warnings.filterwarnings('ignore')


def hash_value(value, hash_key:str):

    '''
    Description: Generates hashed value for given input.

    Parameters:
        value: Value to be hashed.
        hash_key (str): Key to be added to the value.
        
    Returns:
        str: Hashed value.
    '''

    hashed_vale = hashlib.sha256((str(value) + hash_key).encode()).hexdigest()
    
    return hashed_vale



def shift_dates(data: pd.DataFrame, to_shift: list, shifting_dict: dict):

    '''
    Description: Shifts dates by subtracting a random number. It is consistent for each patient.

    Parameters
        data (pd.DataFrame): Dataframe to be modified.
        to_shift (list): List of date columns to shift.
        shifting_dict: Dictionary with corresponding shifting value for each patient.
        
    Returns
        pd.DataFrame: Dataframe with modified dates.
    '''

    data[to_shift] = data[to_shift].apply(pd.to_datetime)
    shifting_df = pd.DataFrame(list(shifting_dict.items()), columns=['pat_id', 'shifting_value'])
    data = data.merge(shifting_df, on='pat_id', how='left')
    for col in to_shift:
        data[col] = data[col] - pd.to_timedelta(data['shifting_value'], unit='d')
    data.drop(['shifting_value'], axis=1, inplace=True)

    return data



def hashing_mapping(data: pd.DataFrame, col: str, mapping_path: str, hash_key: str):

    '''
    Description: Hashes each unique id and saves mapping file.

    Parameters:
        data (pd.DataFrame): Dataframe that contains the unique ids.
        col (str): Name of the column to hash.
        mapping_path (str): Location of the file with the mappings.
        hash_key (str): Key for hashing.
    '''

    # Check if hash mapping file exists
    if os.path.exists(os.path.join(mapping_path, f'{col}_mapping.json')):
        with open(os.path.join(mapping_path, f'{col}_mapping.json'), 'r') as f:
            mapping_dict = json.load(f)
    else:
        mapping_dict = {}

    # Assign hashed values to unique ids
    unique_ids = data[col].unique().tolist()
    unique_ids = [str(id) for id in unique_ids if str(id) not in list(mapping_dict.keys())]
    hashed_values = [hash_value(id, hash_key) for id in unique_ids]
    mapping_dict.update({str(id): value for id, value in zip(unique_ids, hashed_values)})

    # Save updated dictionary
    with open(os.path.join(mapping_path, f'{col}_mapping.json'), 'w') as f:
        json.dump(mapping_dict, f, indent=4)



def shifting_mapping(data: pd.DataFrame, mapping_path: str):

    '''
    Description: Assigns random integer values to each unique id and saves mapping file.

    Parameters:
        data (pd.DataFrame): Dataframe that contains the unique ids.
        mapping_path (str): Location of the file with the mappings.
        
    Return:
        dict: Updated mappings dictionary.
    '''

    # Check if date shifting mapping file exists
    if os.path.exists(os.path.join(mapping_path, 'pat_id_shifting_mapping.json')):
        with open(os.path.join(mapping_path, 'pat_id_shifting_mapping.json'), 'r') as f:
            shifting_values_dict = json.load(f)
    else:
        shifting_values_dict = {}

    # Assign random values to unique pat_ids
    unique_pat_ids = data['pat_id'].unique().tolist()
    unique_pat_ids = [id for id in unique_pat_ids if id not in list(shifting_values_dict.keys())]
    rdm_shifting_values = np.random.randint(1, 185, size=len(unique_pat_ids))
    shifting_values_dict.update({str(pat_id): int(value) for pat_id, value in zip(unique_pat_ids, rdm_shifting_values)})

    # Save updated dictionary
    with open(os.path.join(mapping_path, 'pat_id_shifting_mapping.json'), 'w') as f:
        json.dump(shifting_values_dict, f, indent=4)

    return shifting_values_dict



def parse_arguments():

    '''
    Description: Parses arguments.
    '''

    parser = argparse.ArgumentParser(description='Deidentify EHR file.')
    parser.add_argument('--data_path', type=str, required=True, help='Location of the file.')
    parser.add_argument('--deid_path', type=str, required=True, help='Path of deid files.')
    parser.add_argument('--mapping_path', type=str, required=True, help='Path of mapping files.')

    args = parser.parse_args()

    return args






if __name__ == '__main__':

    '''
    Run from the terminal: python deidentify_ehr.py --data_path /path/to/data --deid_path /path/to/deid/data --mapping_path /path/to/mappings
    '''

    args = parse_arguments()
    data_path = args.data_path
    deid_path = args.deid_path
    mapping_path = args.mapping_path

    # Define columns to deid
    drop_cols = ['name', 'address_1', 'address_2', 'city', 'state', 'zip', 'auth_provider']
    hash_cols = ['pat_id', 'mrn', 'csn']
    shift_cols = ['dob', 'admission_date', 'surgery_date', 'placement_date', 'removal_date', 'entered_dept', 
                'exited_dept', 'hosp_admission', 'hosp_discharge', 'procedure_date', 'order_date', 
                'specimen_taken_time', 'result_date', 'mar_time', 'note_created', 'code_start', 'code_end',
                'update_date', 'death_date', 'noted_date', 'resolved_date', 'order_time', 'recorded_time']
    
    # Define hash_key
    hash_key = '123'

    filenames = [filename for filename in os.listdir(data_path) if '.pkl' in filename]

    for filename in filenames:
            
        try:

            # Read file
            print(f'\nReading {filename}...')
            data = pd.read_pickle(os.path.join(data_path, filename))

            # Select cols to deidentify
            to_drop = [col for col in data.columns if col in drop_cols]
            to_hash = [col for col in data.columns if col in hash_cols]
            to_shift = [col for col in data.columns if col in shift_cols]

            # Shift dates
            print(f'Shifting dates...')
            shifting_values_dict = shifting_mapping(data, mapping_path)
            data = shift_dates(data, to_shift, shifting_values_dict)

            # Drop columns
            print(f'Dropping columns...')
            data.drop(to_drop, axis=1, inplace=True)

            # Hash columns
            print(f'Hashing columns...')
            for col in to_hash:
                hashing_mapping(data, col, mapping_path, hash_key)
                data[col] = data[col].apply(lambda x: hash_value(x, hash_key))

            # Change column names
            col_names = {col:f'{col}_deid' for col in set(to_hash)|set(to_shift)}
            data = data.rename(columns=col_names)

            # Save deid data
            print(f'Saving deid {filename}...')
            data.to_pickle(os.path.join(deid_path, filename))

            print('Done!\n')

        except:

            print(f'\nDeidentification of {filename} failed\n')
            continue

