#!/bin/bash

#This is a very simple script that should never be touched by a user.
#It is simply here so that there is a consistent, generalized script for its
#MASTER to run. This creates the files with the MASTER's help.

INPUT=benchmark.in
OUTPUT=bench.out
. /opt/ohpc/pub/spack/v0.19.1/share/spack/setup-env.sh
spack load namd
source /home/software/namd/namd_functions
namd_setup # loads modules and sets up nodelists as needed
namd_run # runs charmrun or namd2 as needed using ${INPUT} and ${OUTPUT}
