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

    path_to_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/PNG')
    path_to_deid_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/anon')

    path_to_data = path_to_data / str(year)
    path_to_deid_data = path_to_deid_data / str(year)
    path_to_deid_data.mkdir(parents = True, exist_ok = True)
    
    #preprocess metadata
    df = pd.read_csv(path_to_data / 'metadata.csv', usecols = ['AccessionNumber', 'StudyTime', 'SeriesTime'])
    
    df['AccessionNumber'] = df['AccessionNumber'].apply(lambda x: hash_value(x, hash_key))
    
    df.to_csv(path_to_deid_data / 'metadata_matching_times.csv', index = False)

    