#!/bin/bash
#SBATCH -J GdeMR
#SBATCH -p batch,overflow
#SBATCH -t 24:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-8
#SBATCH --mem 72G
#SBATCH -o ./out/grdeid_%a.out
#SBATCH -e ./out/grdeid_%a.err

echo This is the num processes - $SLURM_ARRAY_TASK_COUNT

source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

python deidentification_grady.py --index $SLURM_ARRAY_TASK_ID
