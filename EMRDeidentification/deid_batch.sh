#!/bin/bash
#SBATCH -J deidCXR
#SBATCH -p batch,overflow
#SBATCH -t 24:0:0
##SBATCH --nodes=1
##SBATCH --ntasks=1
#SBATCH --array=0-1
#SBATCH --mem 72G
#SBATCH -o ./out/cxr_deidnotes_%a.out
#SBATCH -e ./out/cxr_deidnotes_%a.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids-24.12

python deidentification_cxr.py --index $SLURM_ARRAY_TASK_ID
