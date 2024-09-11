import pandas as pd 
import os
from pathlib import Path

path_to_combined_meta = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/')
combined_metas = [str(path_to_combined_meta) + f'/Combined_Meta_{year}.pkl' for year in range(2015, 2021)]

for idx, metadf in enumerate(combined_metas):
    print(idx)
    if idx == 0:
        df = pd.read_pickle(metadf)
    else:
        df = pd.concat([df, pd.read_pickle(metadf)], ignore_index=True)

path_to_combined_meta_allyears = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Meta.csv')
df.to_csv(path_to_combined_meta_allyears, index=False)