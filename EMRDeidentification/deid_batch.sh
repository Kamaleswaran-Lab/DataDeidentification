#!/bin/bash
#SBATCH -J demory
#SBATCH -p batch,overflow
#SBATCH -t 24:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-9
#SBATCH --mem 72G
#SBATCH -o ./out/dcxr_2_%a.out
#SBATCH -e ./out/dcxr_2_%a.err

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids-24.12

python deidentification_cxr.py --index $SLURM_ARRAY_TASK_ID
