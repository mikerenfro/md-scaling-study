#!/bin/bash

#This loop gives the names to the files and goes through each one.
for analysis in gromacs lammps namd; do
	#This check keeps the user from redownloading files in the event 
	#of an issue downloading a different one or 
	#simply not wanting to install new folders.
	#It will still attempt to create the new files and links.
	if [ -s ${analysis} ]; then
		echo "File exists. Attempting to create directories."
	else
		wget https://www.hecbiosim.ac.uk/benchmark-files/${analysis}.tar.gz
		tar -xzf ${analysis}.tar.gz
		rm ${analysis}.tar.gz
	fi
	#Looks through each of the newly generated atoms folders
	for atoms in ${analysis}/*-atoms; do
		for cores in 1 2 4 8 14 28 56 112 224 448 896; do
			#Creating the directories for organization
			#And to make code easier.
			mkdir -p ${atoms}/${cores}/
			#Creating symbolic links within each of the folders.
			if [ ${analysis} == gromacs ]; then
				(cd ${atoms}/${cores}; ln -s -f ../benchmark.tpr .)
			elif [ ${analysis} == lammps ]; then
				(cd ${atoms}/${cores}; ln -s -f ../benchmark.* .)
			elif [ ${analysis} == namd ]; then
				(cd ${atoms}/${cores}; ln -s -f ../benchmark.* .; ln -s -f ../*.prm .)
			else
				#This should hopefully never happen.
				#If it does, post an issue to the github.
				>&2 echo "It appears that something has gone wrong." 
			fi	
		done
	done
done