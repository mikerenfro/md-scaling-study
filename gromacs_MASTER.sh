#!/bin/bash

cd gromacs/

#If you want this to only do, for instance, 20k and 3000
#Do "for file in 20k-atoms 3000k-atoms; do"
for file in *-atoms/; do #Going into all of the atom sizes
	#Only doing the smaller ones, designating lots of time (relatively).
	#In general, even the slowest times in gromacs are fast.
	#If --time needs to be increased, only increase the number of hours.
	#This is going into each core folder and starting an sbatch job.
	for cores in 1 2 4; do 
		(cd ${file}/${cores}; sbatch --nodes=1 \
		--cpus-per-task=${cores} --time=28:00:00 \
		../../../gromacs-mc.sh)
	done

	for cores in 8 14 28; do
		(cd ${file}/${cores}; sbatch --nodes=1 \
                --cpus-per-task=${cores} --time=5:00:00 \
                ../../../gromacs-mc.sh)
	done

	#This is different due to how gromacs runs jobs with more than one node
	#After much experimentation, --ntasks was set to 4 and --cpus was
	#set to 7. This was done to optimize speeds and avoids any
	#issues created by doing "large prime factors"
	#The expr is figuring out how many nodes it needs to give it.
	for cores in 56 112 224 448 896; do
		(cd ${file}/${cores}; nodes=$(expr ${cores} / 28);\
		sbatch --nodes=${nodes} --ntasks-per-node=4 --time=01:00:00 \
		--cpus-per-task=7 ../../../gromacs-mpi.sh)
	done

done
