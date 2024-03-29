#!/bin/bash

#Debugging line. Remove pipes to examine further.
#tail -n 5 /bench.log | grep "Time" | awk '{print $3}'

if [ -s gromacs/ ]; then
	#Enters the gromacs directory to limit scope and make code easier.
	cd gromacs/
else
        >&2 echo "ERROR:"
        >&2 echo "It appears the gromacs folder does not exist or is empty."
        >&2 echo "SUGGESTIONS:"
        >&2 echo "Have you run the setup.sh yet?"
        >&2 echo "Is this script where it was when this project was cloned?"
        exit -1
fi

#This scans each atoms folder within the gromacs folder.
#It sends the file it selects with the for-loop into 
#the csvGenerator python script.
#The Python script outputs the data into a csv file.

#FOR DEBUGGING: Put a pound sign before the greater than symbol in order to 
#output to the screen what the csvGenerator would put onto the screen.

for file in *-atoms; do
	python ../csvgenerator.py gromacs ${file}/*/bench*.log > ../${file}_GROMACS_Data.csv
done
