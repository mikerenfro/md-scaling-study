#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
 
INPUT=benchmark.in
OUTPUT=bench28C.out
module load lammps
mpirun --mca btl ^tcp -np ${SLURM_NTASKS} \
    lmp_mpi -in ${INPUT} -log ${OUTPUT}
