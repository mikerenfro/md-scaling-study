#!/bin/bash

INPUT=benchmark.tpr
OUTPUT=bench.log
module load gromacs
gmx mdrun -nt ${SLURM_CPUS_PER_TASK} -s ${INPUT} -g ${OUTPUT}
