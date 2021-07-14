#!/bin/bash

cd lammps/

#If you want this to only do, for instance, 20k and 3000 
#Do "for file in 20k-atoms 3000k-atoms; do"
for file in *-atoms/; do #Going into all of the atom sizes
	#Only doing the smaller ones, designating lots of time (relatively).
        #In general, even the slowest times in gromacs are fast.
        #If --time needs to be increased, only increase the number of hours.
        #This is going into each core folder and starting an sbatch job.
	for cores in 1 2 4; do 
		(cd ${file}/${cores}; sbatch --nodes=1 \
		--ntasks-per-node=${cores} --time=132:00:00 --mem=16G \
		../../../lammps.sh)
	done
	for cores in 8 14 28; do
		(cd ${file}/${cores}; sbatch --nodes=1 \
                --ntasks-per-node=${cores} --time=16:00:00 \
                ../../../lammps.sh)
	done
	for cores in 56 112 224 448 896; do
		(cd ${file}/${cores}; nodes=$(expr ${cores} / 28);\
		sbatch --nodes=${nodes} --ntasks-per-node=28 --time=02:30:00 \
		../../../lammps.sh)
	done
done
