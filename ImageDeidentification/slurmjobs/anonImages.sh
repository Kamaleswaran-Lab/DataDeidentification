#!/bin/bash

#SBATCH -J AnoM10
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 180:0:0
#SBATCH --nodes=1

#SBATCH --mem 64G

#SBATCH -o /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/anonMarch10.out
#SBATCH -e /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/anonMarch10.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids-24.12

cd /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/Niffler/modules/dicom-anonymization/

python DicomAnonymizerHashing.py /labs/collab/Imaging/Imaging-PHI/Emory_Images/ICU_IMAGES /labs/collab/Imaging/Imaging-PHI/Emory_Images/Anon/ICU_IMAGES
