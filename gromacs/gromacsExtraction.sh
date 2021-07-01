#!/bin/bash

#Expect 19 entries due to 20k have 9 entries and 3M having 10 completed entries.
#If 896C on 3M is ever successfully ran, expect 20. 
#20k will still have 9 (as many needed to show decay in performance). 
#3M will have 10 - 11 (showing maximum core usage speedup capability.)

#Debugging line. Remove pipes to examine further.
#tail -n 5 *atoms*/bench*.log | grep "Time" | awk '{print $3}'

python ../csvGenerator.py gromacs 20k-atoms*/bench*.log > ../20k_gromacs_Data.csv

python ../csvGenerator.py gromacs 3000k-atoms*/bench*.log > ../3M_gromacs_Data.csv
