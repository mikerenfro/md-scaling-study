#!/bin/bash

#This is a very simple script that should never be touched by a user.
#It is simply here so that there is a consistent, generalized script for its
#MASTER to run. This creates the files with the MASTER's help.

INPUT=benchmark.in
OUTPUT=bench.out
module load lammps
mpirun --mca btl ^tcp -np ${SLURM_NTASKS} \
	lmp_mpi -in ${INPUT} -log ${OUTPUT}
