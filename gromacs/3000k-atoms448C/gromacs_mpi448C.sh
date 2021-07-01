#!/bin/bash
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=7
#SBATCH --time=00:30:00

INPUT=benchmark.tpr
OUTPUT=bench_mpi.log
module load gromacs
mpirun `which mdrun_mpi` ${SLURM_CPUS_PER_TASK} -s ${INPUT} -g ${OUTPUT}

