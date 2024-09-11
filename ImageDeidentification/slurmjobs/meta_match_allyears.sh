#!/bin/bash

#SBATCH -J metaMatch
#SBATCH -p batch,overflow
#SBATCH -G 0
#SBATCH -t 24:0:0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=0-8

#SBATCH --mem 64G

#SBATCH -o ./OutputErrorFiles/metaMatch_%a.out
#SBATCH -e ./OutputErrorFiles/metaMatch_%a.err

YEARS=(2014 2015 2016 2017 2018 2019 2020 2021 2022)
source /home/maror24/anaconda3/bin/deactivate
source /home/maror24/anaconda3/bin/activate rapids

echo "This task is : $SLURM_ARRAY_TASK_ID"

python dicom_anon_meta.py ${YEARS[$SLURM_ARRAY_TASK_ID]}
