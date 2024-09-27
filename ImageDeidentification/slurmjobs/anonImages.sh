#!/bin/bash

#SBATCH -J Anon 
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 120:0:0
#SBATCH --nodes=1


#SBATCH --mem 64G

#SBATCH -o /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/anon.out
#SBATCH -e /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/anon.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

cd /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/Niffler/modules/dicom-anonymization/

python DicomAnonymizerHashing.py /labs/collab/Imaging/Imaging-PHI/Emory_Images/ImagesWithNotes/ImagesWithNotes /labs/collab/Imaging/Imaging-PHI/Emory_Images/ImagesWithNotes/ImagesWithNotesAnon
