#!/bin/bash

INPUT=benchmark.in
OUTPUT=bench.out
module load lammps
mpirun --mca btl ^tcp -np ${SLURM_NTASKS} \
	lmp_mpi -in ${INPUT} -log ${OUTPUT}
