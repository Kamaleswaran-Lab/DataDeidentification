import pandas as pd 
import os
from pathlib import Path

path_to_radiology_notes = Path('/labs/kamaleswaranlab/MODS/RadiologyNotes/')
radiology_notes = path_to_radiology_notes.glob('*.csv')

for idx, note_set in enumerate(radiology_notes):
    print(idx)
    if idx == 0:
        radiology_notes = pd.read_csv(note_set)
    else:
        radiology_notes = pd.concat([radiology_notes, pd.read_csv(note_set)])

path_to_combined_radiology_notes = Path('/labs/collab/Imaging/Imaging-PHI/Emory_Images/Meta/Combined_Radiology_Notes.csv')
radiology_notes.to_csv(path_to_combined_radiology_notes, index=False)