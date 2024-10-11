#!/bin/bash

#SBATCH -J Anon 
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 120:0:0
#SBATCH --nodes=1


#SBATCH --mem 64G

#SBATCH -o ./OutputErrorFiles/anon_%a.out
#SBATCH -e ./OutputErrorFiles/anon_%a.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

echo "This task is : $SLURM_ARRAY_TASK_ID"

cd /home/maror24/DataDeidentification/ImageDeidentification/Niffler/modules/dicom-anonymization/

python DicomAnonymizerHashing.py /labs/collab/Imaging/Imaging-PHI/Emory_Images/ImagesWithNotes/ImagesWithNotes /labs/collab/Imaging/Imaging-PHI/Emory_Images/ImagesWithNotes/ImagesWithNotesAnon
