#!/bin/bash -login
#SBATCH --job-name="dask_test"
#SBATCH --time=0:01:00
#SBATCH --account=m22oc-staff
#SBATCH --partition=standard
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --qos=standard

OMP_NUM_THREADS=1
source /mnt/lustre/indy2lfs/work/m22oc/m22oc/dmckayk/.bashrc_node
conda activate
echo "Running Python"
pwd
which python
python Practical3c.py
