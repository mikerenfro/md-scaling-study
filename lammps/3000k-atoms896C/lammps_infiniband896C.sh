#!/bin/bash
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=28
#SBATCH --time=01:30:00
 
INPUT=benchmark.in
OUTPUT=bench896C.out
module load lammps
mpirun --mca btl ^tcp -np ${SLURM_NTASKS} \
    lmp_mpi -in ${INPUT} -log ${OUTPUT}
