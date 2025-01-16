import pandas as pd
from pathlib import Path
from argparse import ArgumentParser

from emrd import hash_value
from multiprocessing import Pool, cpu_count
import shutil

def rename_png(file):
    file_name_parts = file.split('_')
    file_name_parts[0] = hash_value(file_name_parts[0], hash_key)
    new_file_name = '_'.join(file_name_parts)
    return new_file_name

def copy_file(file):
    file_name = file.stem
    new_file_name = rename_png(file_name)
    new_file_path = path_to_deid_data / (new_file_name + '.png')
    shutil.copy(file, new_file_path)
    print(f'Copied {file} to {new_file_path}')
    

hash_key = '123'
YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
if __name__ == "__main__":
    path_to_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/PNG')
    path_to_deid_data = Path('/labs/collab/Imaging/Imaging-PHI/chest_xrays/anon')

    parser = ArgumentParser()
    parser.add_argument('--index', type = int, required = True)
    args = parser.parse_args()
    year = YEARS[args.index]
    print(year)

    path_to_data = path_to_data / str(year)
    path_to_deid_data = path_to_deid_data / str(year) / 'extracted-images'
    path_to_deid_data.mkdir(parents = True, exist_ok = True)

    files = list(path_to_data.glob('extracted-images/*.png'))

    print(f'Copying {len(files)} files')
    
    num = cpu_count()
    with Pool(num) as p:
        p.map(copy_file, files)


    

