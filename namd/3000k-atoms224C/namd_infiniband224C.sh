#!/bin/bash
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=28
#SBATCH --time=01:30:00
 
INPUT=benchmark.in
OUTPUT=bench224C.out
source /cm/shared/apps/namd/namd_functions
namd_setup # loads modules and sets up nodelists as needed
namd_run # runs charmrun or namd2 as needed using ${INPUT} and ${OUTPUT}
