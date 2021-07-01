#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=14
 
INPUT=benchmark.tpr
OUTPUT=bench.log
module load gromacs
gmx mdrun -nt ${SLURM_CPUS_PER_TASK} -s ${INPUT} -g ${OUTPUT}
