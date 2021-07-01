#!/usr/bin/env python
# coding: utf-8

# In[34]:


import math
import collections

import numpy as np
import matplotlib.pyplot as plt
import glob

    #Naming Scheme of csvs: [FileDescriptor]_[ANALYSISTOOL]_Data.csv
    #If you want everyting, do *Data.csv or
    #If you just want everything done under one File Descriptor,
    #do 3M*Data.csv
    #Data.csv is to avoid getting random csvs mixed in. 

def main():
    style_list='osv^<>8phHD'
 
    plt.figure(figsize=[12,9])
    plt.figure(1)
    
    fileNames = sorted(glob.glob('*Data.csv'))
    
    #analysisTool = "" Not needed in this current iteration.
    i = 0
    for file in fileNames:
        i += 1
        nameSplit = file.split('_')
        name = '{1} ({0} atoms)'.format(nameSplit[0],nameSplit[1])
        #analysisTool = nameSplit[1] We would need something like this, preferably in each for-loop,
        #if we wanted to begin trying to seperate the graphs.
        #This would also need something to seperate the graphs in pyplot, too.
        #In the current state, it would still put everything into into one graph each.
        print(name)
        #fname is the name of the file.
        #I declare commas (,) as the delimiter (as is normal for a csv file)
        #Finally, I skip the header by including "skiprows=1"
        data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
        speedUp(data, name, style=style_list[i]) #Going into the processing function with data
        
    ax = plt.gca()
    
    ax.set_xlabel('Number of Cores')
    ax.set_xscale('log',base=10)
    
    ax.set_ylabel('Speed Up Factor')
    ax.set_yscale('log',base=10)
    
    plt.legend()
    plt.savefig(fname="speedUp.pdf")
    
    plt.figure(figsize=[12,9])
    plt.figure(2)
    
    fileNames = sorted(glob.glob('20k*Data.csv')) 
    
    i = 0 
    for file in fileNames:
        i += 1
        nameSplit = file.split('_')
        name = '{1} ({0} atoms)'.format(nameSplit[0],nameSplit[1])
        data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
        wallTime(data, name, style=style_list[i])

    ax = plt.gca()
    
    ax.set_xlabel('Number of Cores')
    ax.set_xscale('log',base=10)
    
    ax.set_ylabel('Walltime of Job')
    ax.set_yscale('log',base=10)
    
    plt.legend() 
    plt.savefig(fname="20k_walltime.pdf") 
    
    plt.figure(figsize=[12,9])
    plt.figure(3)

    fileNames = sorted(glob.glob('3M*Data.csv'))       
    
    i = 0
    for file in fileNames:
        i += 1
        nameSplit = file.split('_')
        name = '{0} ({1} atoms)'.format(nameSplit[0],nameSplit[1])
        data = np.loadtxt(fname=file,delimiter=',',skiprows=1)
        wallTime(data, name, style=style_list[i])

    ax = plt.gca()
    
    ax.set_xlabel('Number of Cores')
    ax.set_xscale('log',base=10)
    
    ax.set_ylabel('Walltime of Job')
    ax.set_yscale('log',base=10)
    
    plt.legend()
    plt.savefig(fname="3M_walltime.pdf")
    
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
    
#Standard Python stuff; checks if the program is in main or not.
if __name__ == "__main__":
    main()




