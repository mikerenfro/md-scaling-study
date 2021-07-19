#!/bin/bash

#This is a very simple script that should never be touched by a user.
#It is simply here so that there is a consistent, generalized script for its
#MASTER to run. This creates the files with the MASTER's help.

INPUT=benchmark.tpr
OUTPUT=bench.log
module load gromacs
gmx mdrun -nt ${SLURM_CPUS_PER_TASK} -s ${INPUT} -g ${OUTPUT}
