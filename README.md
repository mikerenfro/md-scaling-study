# Scaling Study

A batch of python and shell scripts which together create graphs by using data from only **20k and 3000k atom data sets from gromacs, lammps, and namd** programs.

## Usage

The purpose of this is to be easy to use for the three analysis tools that are implemented as of now. 

#### Step One:

Clone this repository for access to the shell scripts that will do most of the work.
Run the setup.sh script and it will download all the needed files, build the directories, and link data to files.
The script will download the gromacs, lammps, and namd data sets from the website. The setup.sh script can take around 15 minutes to complete.

```
./setup.sh
```

#### Step Two:

Once the data is compiled, run the MASTER scripts to create data files for the scalability tests.
This will take approximately 4.5 days, mostly due to the 1 to 4 core scripts on the 3000k models.

```
./gromacs_MASTER.sh
```

#### Step Three: 

With the data compiled, the data extraction scripts can be run. 
This will create new .csv files that can be used for time and speedup comparisons.

```
./gromacsExtraction.sh 
```

Assuming the data is in the correct place, the script will create .csv files in the main directory with all the other scripts.

**NOTE: This WILL override any .csv files that already exist within that directory.** 

#### Step Four:

With the csv files created, the last step would be to create graphs and make the data more human-readable.
Running the following command will create said graphs.
To run the Python script, load the module "anaconda".

```
module load anaconda
python scalability_plotter.py
```

With the csv files in the correct place, the python script should be able to be run.  
After running the Python script, .pdf files should appear that have graphs representing the speedup of the various analysis tools. 
The realtime/walltime spent processing for the various atom sizes will also be present and compared by analysis tool. 

#### Common Issues and the Fixes

There are a few problems identified in the process of making these scripts.
This section will attempt to provide some insight.

###### sbatch Job Failure

There are a variety of reasons the job script can fail:

1. Make sure the setup ran properly and downloaded all the needed materials for the scripts to run.
2. If the scripts tried to run and fail, try to open the slurm script and see if:
   - The job could have run out of time. Go into the MASTER script and give the --time command additional hours. 
   - The job could have run out of memory. Go into the MASTER script and add/modify the --mem to be a greater value than the defaults.

###### Graphs With Distorted or Missing Data

The only documented issue of this happening, if everything else has gone correctly, is due to missing data entries.
The code will default to -1 for walltime if there is nothing there. Due to the way the graphs are built, this will cause the data point to not appear.

If the job that is missing a data point did complete, then perhaps the python script is not looking far enough into the data file:
1. Enter into the csvGenerator.py script
2. Use a search of any kind to find the "readFile.readlines()" line.
3. There will be a negative number within square brackets; make that number larger and that might fix the problem.
   - For reference, that number determines how many lines at the end of the file it searches for the time.


#### Conclusion

The intent of this process was to be as easy to reproduce and run as possible.
Running the scripts in this order should allow one to easily create the graphs needed for a scalability test.

This process may take around **5 days** in total due to the processing times. 
