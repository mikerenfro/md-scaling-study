#!/bin/bash

INPUT=benchmark.in
OUTPUT=bench.out
source /cm/shared/apps/namd/namd_functions
namd_setup # loads modules and sets up nodelists as needed
namd_run # runs charmrun or namd2 as needed using ${INPUT} and ${OUTPUT}