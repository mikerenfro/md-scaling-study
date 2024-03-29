#!/bin/bash

#This is an attempt at keeping a user from accidentally running this script
#before they have run the setup.sh.
#This would likely not even be able to run the jobs, but this stops any
#possibility of the slurm scheduler being filled with empty jobs.
if [ -s lammps/ ]; then
        #Enters the lammps directory to limit scope and make code easier.
        cd lammps/
else
        >&2 echo "ERROR:"
        >&2 echo "It appears the lammps folder does not exist or is empty."
        >&2 echo "SUGGESTIONS:"
        >&2 echo "Have you run the setup.sh yet?"
        >&2 echo "Is this script where it was when this project was cloned?"
        exit -1
fi

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
	for cores in 56 112 224; do
		(cd ${file}/${cores}; nodes=$(expr ${cores} / 28);\
		sbatch --nodes=${nodes} --ntasks-per-node=28 --time=02:30:00 \
		../../../lammps.sh)
	done

	for cores in 448 896; do
		(cd ${file}/${cores}; nodes=$(expr ${cores} / 28);\
		sbatch --nodes=${nodes} --ntasks-per-node=28 --time=00:30:00 \
		../../../lammps.sh)
	done
done
