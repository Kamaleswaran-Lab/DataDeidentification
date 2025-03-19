#!/bin/bash

#SBATCH -J SummaryGrady
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 120:0:0
#SBATCH --nodes=1

#SBATCH --mem 64G

#SBATCH -o /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/summaryGrady.out
#SBATCH -e /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/OutputErrorFiles/summaryGrady.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids-24.12

cd /home/maror24/ImageAnon/DataDeidentification/ImageDeidentification/

pwd

python folder_summary.py /labs/collab/Imaging/Imaging-PHI/Grady_Images

