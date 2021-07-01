#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16G
#SBATCH --time=132:00:00
 
INPUT=benchmark.in
OUTPUT=bench1C.out
source /cm/shared/apps/namd/namd_functions
namd_setup # loads modules and sets up nodelists as needed
namd_run # runs charmrun or namd2 as needed using ${INPUT} and ${OUTPUT}
