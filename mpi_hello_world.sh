#!/bin/bash

#SBATCH --job-name=mpi_test
#SBATCH --partition=workq
#SBATCH --nodes=1
#SBATCH --mem=64GB
#SBATCH --time=00:20:00

echo "before activation: $(which python)"

# Load Cray programming environment and MPI
module load PrgEnv-cray/8.6.0
module load craype-network-ofi
module load cray-mpich

# Activate your conda environment
source ~/miniforge3/bin/activate
conda activate mpi_env

# Reinstall mpi4py from source to link to Cray MPI
pip uninstall -y mpi4py
MPICC=cc pip install --no-binary=mpi4py mpi4py

echo "after activation: $(which python)"

# Run MPI script on 72 processes
srun -n 72 python mpi_hello_world.py