#!/bin/bash
#SBATCH -J MetaNiffler
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 48:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0

#SBATCH --mem 64G

#SBATCH -o ../OutputErrorFiles/meta.out
#SBATCH -e ../OutputErrorFiles/meta.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

echo "This task is : $SLURM_ARRAY_TASK_ID"

cd ../Niffler/modules/png-extraction/
python ImageMetaExtractor.py