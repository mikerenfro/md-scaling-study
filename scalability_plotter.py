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
        #An iterable list of the model sizes
        #This is designed for walltime graphs
    toolsToDo = ["GROMACS","LAMMPS","NAMD"]
        #An iterable list of analysis tools
        #This is designed for speedup graphs
    

    for model in modelsToDo: #Moves through the loops using the iterable list
        figureCreator(model) #Calling the function that creates the graphs
    
    for tool in toolsToDo: 
        figureCreator(tool)

def speedUp(data, name, style):  
    numCores = data[:,0] #All entries of the first column
    wallTime = data[:,1] #All entries of the second column
    
    #Calculating Speed Up of the data.
    speedUp = (data[0,1]/wallTime)

    #Creates the image via take the log2 of the entire data set's
    #first and second column, turning that directly into an image.
    plt.loglog(numCores,speedUp,style,label=name) #Making the plot to be a loglog graph
                                                  #This is used later to make them log2
                                                  #The label=name is what give the legend info to present.

def wallTime(data, name, style):  
    numCores = data[:,0]
    wallTime = data[:,1]
    #For dynamic iteration
    #Creates number of rows and columns in order to iterate through the for loop.
    #Perhaps an iterator would be better.
    plt.loglog(numCores,wallTime,style,label=name)

def figureCreator(wildcard):
                  #TODO: Make this have more options. Should more model sizes be added, this will not work. 
    styleList = { #The list for styles to be used for the graph creation
        0 : "o",
        1 : "^",
        2 : "s",
        3 : "p",
        4 : "*"
    }
    counter = 0 #The counter that keeps track of which style to use

    plt.figure() #The beginning of the graph figures. Without this, the very first graph would not generate
    plt.tight_layout() #This establishes that ALL graphs must be in the tight layout, reducing margins

    ax = plt.gca() #Setting up the axis that the loops can modify to add labels to the graph

    if 'k' in wildcard: #Checking if this is a model size, as all of them have "k"
                        #As in 20k has 20'k', and so on with others
                        #All analysis tools are fully capitalized, so even if a new tool is added with a k
                        #The capitalized analysis tool should fail this check
        fileNames = glob.glob(wildcard+'*.csv') #Grabbing all csvs that have model sizes at the start
        sort_nicely(fileNames) #Sorting the file names using a function taken from github

        plt.title("Walltime for {0} Atoms".format(wildcard)) #Creating a title for the model size

        for file in fileNames: #Looping through a file of a particular model size and gathering times
            (_,solver,_) = file.split('_',2) #Grabbing the name of the analysis tool 
            name = '{0} ({1} atoms)'.format(solver,wildcard) #This is for debugging, for the most part.
                                                             #It tells both future maintainers and the user that
                                                             #a certain part is processing. It can be removed if
                                                             #it is decided that it is not needed.
            print(name)
            data = np.loadtxt(fname=file,delimiter=',',skiprows=1) #This is loading the text from the selected file
            data = data[np.argsort(data[:,0])] #TODO: This is... probably redundant? As the coder, I want to say this line is unneeded.
                                               #I am leaving it here only because I do not want to break it.
                                               #This is, at best, a note to my future self to try to remove it and this comment.
            wallTime(data, "{0}".format(solver),
                     style='{0}-'.format(styleList[counter])) #TODO: This calls the wallTime function with data, which is a singular file
                                                              #with a redundant usage of format that SHOULD be removed
            counter+=1 #Adding one to the style counter which changed to the next style

        savedName = (wildcard+"wallTime.png") #This is a variable which is specific to this if statement that correctly names the save file.
                                             
        ax.set_ylabel('Walltime of Job (s)') #This is to properly label the y axis with Walltime oriented names.
        ax.set_yscale('log',base=10) #Setting this log to be base 10

    else:
        fileNames = sorted(glob.glob('*'+wildcard+'*.csv'))
        
        sort_nicely(fileNames)

        plt.title("Speedup for {0}".format(wildcard))

        for file in fileNames:
            (atoms,_,_) = file.split('_',2) #Splitting the name of the file like above
            atoms = atoms.split('-')[0] #Splitting the 20k from the -atoms it is connected to
            name = '{0} ({1} atoms)'.format(wildcard,atoms)
            print(name)
            data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
            data = data[np.argsort(data[:,0])] #TODO: Figure out if this can be removed
            speedUp(data, '{0} Atoms'.format(atoms),
                     style='{0}-'.format(styleList[counter]))
            counter+=1

        savedName = (wildcard+"Speedup.png")

        ax.set_ylabel('Speedup of Job')
        ax.set_yscale('log',base=10)


    ax.set_xlabel('Number of Cores') #There is always the number of cores for both operations at the bottom
    ax.set_xscale('log',base=10) 

    plt.grid(which='both') #Creating a grid that shows both "major" and "minor" parts
                           #In other words, it is showing the 10s and all the numbers in between

    plt.legend() #Opening the legend. The labels for the legend were created in the wallTime and speedUp functions, to clarify again.

    plt.savefig(fname=savedName) #Saving the file name based on what conditional statement it entered.

###This is code was not produced by Tennessee Tech.            
###Sourced from: https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically/4623518#4623518
###Credit to https://stackoverflow.com/users/9453/daniel-dipaolo
###
###It is a generic sorting algorithm that modifies the lists within themselves, thus it does not need to return anything.
###It sorts the glob lists via human-numerical sort so that the 20k-3000k goes in order.
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




