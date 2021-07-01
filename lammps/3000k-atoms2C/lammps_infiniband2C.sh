#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem=16G
 
INPUT=benchmark.in
OUTPUT=bench2C.out
module load lammps
mpirun --mca btl ^tcp -np ${SLURM_NTASKS} \
    lmp_mpi -in ${INPUT} -log ${OUTPUT}
