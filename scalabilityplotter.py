#!/usr/bin/env python
# coding: utf-8

import math
import collections

import numpy as np
import matplotlib.pyplot as plt
import glob
import re

import warnings
warnings.filterwarnings("error")

# Naming Scheme of csvs: [FileDescriptor]_[ANALYSISTOOL]_Data.csv
# If you want everyting, do *Data.csv or
# If you just want everything done under one File Descriptor,
# do 3000k*Data.csv
# Data.csv is to avoid getting random csvs mixed in.


def main():
    # An iterable list of the models;
    # this is designed for wall time graph
    models_to_do = ["20k", "61k", "465k", "1400k", "3000k"]
    # An iterable list of the analysis tools;
    # this is designed for speedup graph
    tools_to_do = ["GROMACS", "LAMMPS", "NAMD"]

    # Moves through the loops using the iterable list
    for model in models_to_do:
        figure_creator(model)  # Calling the function that creates the graphs

    for tool in tools_to_do:
        figure_creator(tool)


def speedup_calc(data, name, style):
    num_cores = data[:, 0]  # All entries of the first column
    wall_time = data[:, 1]  # All entries of the second column

    # Calculating Speedup of the data.
    speedup = (data[0, 1]/wall_time)

    # Creates the image using the first and second column,
    # turning that directly into an image.
    # Also, makes the plot to be a loglog graph
    # This is used later to make them log2
    # The label=name is what give the legend info to present.

    plt.loglog(num_cores, speedup, style, label=name)


def wall_time_calc(data, name, style):
    num_cores = data[:, 0]
    wall_time = data[:, 1]
    # For dynamic iteration
    # Creates number of rows and columns
    # in order to iterate through the for loop.
    # Perhaps an iterator would be better.
    plt.loglog(num_cores, wall_time, style, label=name)


def figure_creator(wildcard):
    # Makes two style lists to reference against when making plots
    marker = ["o","^","s","p","*"]
    line_style = ["-",":","--"]

    # The beginning of the graph figures.
    # Without this, the very first graph would not generate
    plt.figure()
    # This establishes that ALL graphs
    # must be in the tight layout, reducing margins
    plt.tight_layout()

    # Setting up the axis that the loops can modify to add labels to the graph
    ax = plt.gca()

    # Checking if this is a model size,
    # as all of them have "k"
    # As in 20k has 20'k', and so on with others
    # All analysis tools are fully capitalized,
    # so even if a new tool is added with a k
    # The capitalized analysis tool should fail this check
    if 'k' in wildcard:
        # Moving into the function,
        # which should provide easier readability.
        # The if expression is to catch failed glob attempts.
        success_check = (create_wall_time_figure(wildcard, style_list))
        if success_check is False:
            return
        # The else is to resolve when it was successful 
        else:
            # This is a variable which is specific to this
            # if statement that correctly names the save file.
            saved_name = (wildcard+"walltime.png")
            # This is to properly label the y axis
            # with wall time oriented names.
            ax.set_ylabel('Walltime of Job (s)')
            # Setting this log to be base 10
            ax.set_yscale('log', base=10)

    else:
        success_check = (create_speedup_figure(wildcard, style_list))
        if success_check is False:
            return            
        else:
            saved_name = (wildcard+"speedup.png")
            ax.set_ylabel('Speedup of Job')
            ax.set_yscale('log', base=10)

    # There is always the number of cores
    # for both operations at the bottom
    ax.set_xlabel('Number of Cores')
    ax.set_xscale('log', base=10)

    # Creating a grid that shows both "major" and "minor" parts
    # In other words, it is showing the 10s
    # and all the numbers in between
    plt.grid(which='both')

    # Opening the legend.
    # The labels for the legend were created in
    # the wall time and speedup functions, to clarify again.
    plt.legend()

    # Saving the file name based on
    # what conditional statement it entered.
    plt.savefig(fname=saved_name)


def create_wall_time_figure(wildcard, style_list):
    # Grabbing all csvs that have model sizes at the start
    file_names = glob.glob(wildcard+'*.csv')

    # Checking if the glob was able to find anything and create the list.
    if not file_names:
        print("ERROR:\nIt appears that there are no", wildcard, "csv files.")
        print("If this is unexpected, try running the Extraction scripts.")
        print("Otherwise, refer to the README.md for help.")
        return False

    # Sorting the file names using a function taken from github
    sort_nicely(file_names)

    # Creating a title for the model size
    plt.title("Walltime for {0} Atoms".format(wildcard))

    success = False # Attempts to keep bad data from creating empty graphs
    counter = 0  # Iterates through the style_list
    # Looping through a file of a particular model size and gathering times
    for file in file_names:
        # Grabbing the name of the analysis tool
        (_, solver, _) = file.split('_', 2)
        name = '{0} ({1} atoms)'.format(solver, wildcard)
        # This is for debugging, for the most part.
        # It tells both future maintainers and the user that
        # a certain part is processing. It can be removed if
        # it is decided that it is not needed.
        print(name)
        # Attempting to stop a single bad csv from killing the program.
        try:
            # This is loading the text from the selected file
            data = np.loadtxt(fname=file, delimiter=',', skiprows=1)
        except ValueError:
            # This error is to catch bad data,
            # like a string or other problematic type.
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv has bad (or otherwise unreadable) data.")
            continue
        except StopIteration:
            # This is to catch empty csv files.
            # StopIteration is an entirely empty csv (uncommon)
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv is empty.")
            continue
        except IndexError:
            # IndexError is when there is a header but nothing else (more common)
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv is empty.")
            continue
        except UserWarning:
            # There seems to be a final edge case that somehow
            # does not cause errors until here. This is to catch that.
            # This error should be caught by IndexError, but
            # This does not happen for some reason.
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears that no data successfully loaded.")
            continue
        # A required additional sort that manages
        # datapoints on the graphs,
        # making them ordered
        success = True
        data = data[np.argsort(data[:, 0])]
        wall_time_calc(data, solver,
                       sstyle=marker[counter]+line_style[counter%3]))
        counter += 1  # incrementing the counter for style_list
    return success


def create_speedup_figure(wildcard, style_list):
    file_names = sorted(glob.glob('*'+wildcard+'*.csv'))

    # It should never be able to reach here if this is the case,
    # but it is conceptually possible.
    if not file_names:
        print("ERROR:\nIt appears that there are no", wildcard, "csv files.")
        print("If this is unexpected, try running the Extraction scripts.")
        print("Otherwise, refer to the README.md for help.")
        return False

    sort_nicely(file_names)

    plt.title("Speedup for {0}".format(wildcard))

    counter = 0
    for file in file_names:
        # Splitting the name of the file like above, but
        (atoms, _, _) = file.split('_', 2)
        # splitting the 20k from the -atoms it is connected to.
        atoms = atoms.split('-')[0]
        name = '{0} ({1} atoms)'.format(wildcard, atoms)
        print(name)
        try:
            # This is loading the text from the selected file
            data = np.loadtxt(fname=file, delimiter=',', skiprows=1)
        except ValueError:
            # This error is to catch bad data,
            # like a string or other problematic type.
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv has bad (or otherwise unreadable) data.")
            continue
        except StopIteration:
            # This is to catch empty csv files.
            # StopIteration is an entirely empty csv (uncommon)
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv is empty.")
            continue
        except IndexError:
            # IndexError is when there is a header but nothing else (more common)
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears the csv is empty.")
            continue
        except UserWarning:
            # There seems to be a final edge case that somehow
            # does not cause errors until here. This is to catch that.
            # This error should be caught by IndexError, but
            # This does not happen for some reason.
            print("ERROR:\n" + file, "cannot be loaded.")
            print("It appears that no data successfully loaded.")
            continue
        data = data[np.argsort(data[:, 0])]
        speedup_calc(data, '{0} Atoms'.format(atoms),
                style='{0}-'.format(style_list[counter]))
        counter += 1
    return True

# This is code was not produced by Tennessee Tech.
# Sourced from: https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically/4623518#4623518
# Credit to https://stackoverflow.com/users/9453/daniel-dipaolo
#
# It is a generic sorting algorithm that modifies the lists within themselves
# thus it does not need to return anything.
# It sorts the glob lists via human-numerical sort,
# so that the 20k-3000k goes in order.


def try_int(s):
    try:
        return int(s)
    except Exception:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [try_int(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(L):
    """ Sort the given list in the way that humans expect.
    """
    L.sort(key=alphanum_key)


# Standard Python stuff; checks if the program is in main or not.
if __name__ == "__main__":
    main()
