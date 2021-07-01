# Scaling Study

A batch of python and shell scripts which together create graphs by using data from only **20k and 3000k atom data sets from gromacs, lammps, and namd** programs.

## Usage

The purpose of this is to be easy to use for the three analysis tools that are implemented as of now. 

#### Step One:

Clone this repository for access to the folders where data should go and the shell scripts that will attempt to process said data.
Insert the data for gromacs, lammps, and namd to run. 

#### Step Two:

From there, run the pre-made shell scripts that will begin the processing of the data.
The commands would be, with lammps for example:

```
./lammpsExtraction.sh
```
Assuming the data is in the correct place, it should have created .csv files in the previous directory, where the python scripts are.

#### Step Three:

To run the Python script, load the module "anaconda".
With the csv files in the correct place, the python script should be able to be run.  
After running the Python script, .pdf files should appear that have graphs representing the speedup of the various analysis tools, as well as various realtime spent processing for the various atom sizes. 

The commands would be:
```
module load anaconda
python scalability_plotter.py
```

#### Conclusion

Hopefully, this process is simple and easy to understand. The running of the shell scripts to create the data, if the data was not already created or new input files were added, will take *upwards of 4.5 days*, particularly with the *<4 Core counts*.

If the data is already completed and ready, then the process of making the data into readable graphs should take within 5 minutes.