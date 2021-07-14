#!/bin/bash

cd lammps #Enters the lammps directory to limit scope and make code easier.

#This scans each atoms folder within the lammps folder.
#It sends the file it selects with the for-loop into
#the csvGenerator python script.
#The Python script outputs the data into a csv file.

#FOR DEBUGGING: Put a pound sign before the greater than symbol in order to
#output to the screen what the csvGenerator would put onto the screen.
for file in *-atoms; do
	python ../csvGenerator.py lammps ${file}/*/bench.out > ../${file}_LAMMPS_Data.csv
done
