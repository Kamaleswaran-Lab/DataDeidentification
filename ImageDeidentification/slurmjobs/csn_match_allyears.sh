#!/bin/bash

#SBATCH -J csnMatch
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 48:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-3

#SBATCH --mem 64G

#SBATCH -o ./OutputErrorFiles/csnMatch_%a.out
#SBATCH -e ./OutputErrorFiles/csnMatch_%a.err

YEARS=(2015 2016 2017)   #(2014 2015 2016 2017 2018 2019 2020 2021 2022)
source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

echo "This task is : $SLURM_ARRAY_TASK_ID"

python dicom_match_time_csn.py ${YEARS[$SLURM_ARRAY_TASK_ID]}
