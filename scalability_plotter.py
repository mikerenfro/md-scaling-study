#!/usr/bin/env python
# coding: utf-8

import math
import collections

import numpy as np
import matplotlib.pyplot as plt
import glob
import re

    #Naming Scheme of csvs: [FileDescriptor]_[ANALYSISTOOL]_Data.csv
    #If you want everyting, do *Data.csv or
    #If you just want everything done under one File Descriptor,
    #do 3000k*Data.csv
    #Data.csv is to avoid getting random csvs mixed in. 

def main():
    modelsToDo = ["20k","61k","465k","1400k","3000k"]
    toolsToDo = ["GROMACS","LAMMPS","NAMD"]
    counter = 0

    for model in modelsToDo:
        figureCreator(model)
    
    for tool in toolsToDo:
        figureCreator(tool)

def speedUp(data, name, style):  
    numCores = data[:,0]
    wallTime = data[:,1] 
    
    #Calculating Speed Up of the data.
    speedUp = (data[0,1]/wallTime)

    #Creates the image via take the log2 of the entire data set's
    #first and second column, turning that directly into an image.
    plt.loglog(numCores,speedUp,style,label=name)
    
def wallTime(data, name, style):  
    numCores = data[:,0]
    wallTime = data[:,1]
    #For dynamic iteration
    #Creates number of rows and columns in order to iterate through the for loop.
    #Perhaps an iterator would be better.
    plt.loglog(numCores,wallTime,style,label=name)

def figureCreator(wildcard):
    styleList = {
        0 : "o",
        1 : "^",
        2 : "s",
        3 : "p",
        4 : "*"
    }
    counter = 0

    plt.figure()
    plt.tight_layout()

    ax = plt.gca()

    if 'k' in wildcard:
        fileNames = glob.glob(wildcard+'*.csv')
        sort_nicely(fileNames)

        plt.title("Walltime for {0} Atoms".format(wildcard))

        fileNames

        for file in fileNames:
            (_,solver,_) = file.split('_',2)
            name = '{0} ({1} atoms)'.format(solver,wildcard)
            print(name)
            data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
            data = data[np.argsort(data[:,0])]
            wallTime(data, "{0}".format(solver),
                     style='{0}-'.format(styleList[counter]))
            counter+=1

        savedName = (wildcard+"wallTime.png")

        ax.set_ylabel('Walltime of Job (s)')
        ax.set_yscale('log',base=10)

    else:
        fileNames = sorted(glob.glob('*'+wildcard+'*.csv'))
        
        sort_nicely(fileNames)

        plt.title("Speedup for {0}".format(wildcard))

        for file in fileNames:
            (atoms,_,_) = file.split('_',2)
            atoms = atoms.split('-')[0]
            name = '{0} ({1} atoms)'.format(wildcard,atoms)
            print(name)
            data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
            data = data[np.argsort(data[:,0])]
            speedUp(data, '{0} Atoms'.format(atoms),
                     style='{0}-'.format(styleList[counter]))
            counter+=1

        savedName = (wildcard+"Speedup.png")

        ax.set_ylabel('Speedup of Job')
        ax.set_yscale('log',base=10)


    ax.set_xlabel('Number of Cores')
    ax.set_xscale('log',base=10)

    plt.grid(which='both')

    plt.legend()

    plt.savefig(fname=savedName)
            
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


#Standard Python stuff; checks if the program is in main or not.
if __name__ == "__main__":
    main()




