#!/bin/bash
#SBATCH -J MetaEmory
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 72:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0

#SBATCH --mem 128G

#SBATCH -o ../OutputErrorFiles/metaEmoryJune14_1.out
#SBATCH -e ../OutputErrorFiles/metaEmoryJune14_1.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids-24.12

echo "This task is : $SLURM_ARRAY_TASK_ID"

cd ../Niffler/modules/png-extraction/
python ImageMetaExtractor.py
