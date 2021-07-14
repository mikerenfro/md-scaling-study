#!/bin/bash

INPUT=benchmark.tpr
OUTPUT=bench_mpi.log
module load gromacs
mpirun `which mdrun_mpi` ${SLURM_CPUS_PER_TASK} -s ${INPUT} -g ${OUTPUT}
