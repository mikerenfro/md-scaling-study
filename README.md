# Scaling Study

A batch of python and shell scripts which together create graphs by using any model size data from only **GROMACS, LAMMPS, and NAMD** programs.

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
python scalabilityplotter.py
```

With the csv files in the correct place, the python script should be able to be run.  
After running the Python script, .png (or, if you changed it, some other desired file type) files should appear that have graphs representing the speedup of the various analysis tools. 
The real/wall time spent processing for the various atom sizes will also be present and compared by analysis tool. 

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
The code will default to setting the value to None, which removes the data point from the graph. 
The graph will maintain its general style, but the missing data point will be a blank spot between others or at either ends.

If the job that is missing a data point did complete, then perhaps the python script is not looking far enough into the data file:
1. Enter into the csvgenerator.py script
2. Either search or go to the time_finder function itself and try to find "f.readlines() [-5:]" (line 67).
3. There will be a negative number within square brackets; make that number larger (as in -5 to -10) and that might fix the problem.
   - For reference, that number determines how many lines at the end of the file it searches for the time.

###### Outputting Undesired Data Format for Graphs

This potential issue is a relatively easy fix, although it does involve modifying the Python code, should this be needed:
1. Enter into the scalabilityplotter.py script
2. Use a search of any kind to find **BOTH** "saved_name" variables (line 94 and 117).
3. The saved_name will have "descriptor.type"; change the "type" to pdf, png, jpg, or the file type it needs.
   - Example: "saved_name = (wildcard+"wall_time.png")" into "saved_name = (wildcard+"wall_time.pdf")"
   - Be aware that there is a possibility that the function that creates the graphs will not be able to create the exact desired file format. There is little that can be done about this. 

#### Conclusion

The intent of this process was to be as easy to reproduce and run as possible.
Running the scripts in this order should allow one to easily create the graphs needed for a scalability test.

This process may take around **5 days** in total due to the processing times. 
