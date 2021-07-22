#!/usr/bin/env python
# coding: utf-8

import math
import collections

import numpy as np
import matplotlib.pyplot as plt
import glob
import re

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
    # TODO: Make this have more options:
    # Should more model sizes be added, this will not work.
    style_list = {  # The list for styles to be used for the graph creation
        0: "o",
        1: "^",
        2: "s",
        3: "p",
        4: "*"
    }

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
        create_wall_time_figure(wildcard, style_list)
        # This is a variable which is specific to this
        # if statement that correctly names the save file.
        saved_name = (wildcard+"walltime.png")
        # This is to properly label the y axis
        # with wall time oriented names.
        ax.set_ylabel('Walltime of Job (s)')
        # Setting this log to be base 10
        ax.set_yscale('log', base=10)

    else:
        create_speedup_figure(wildcard, style_list)
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
    # Sorting the file names using a function taken from github
    sort_nicely(file_names)

    # Creating a title for the model size
    plt.title("Walltime for {0} Atoms".format(wildcard))

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
        # This is loading the text from the selected file
        data = np.loadtxt(fname=file, delimiter=',', skiprows=1)
        # A required additional sort that manages
        # datapoints on the graphs,
        # making them ordered
        data = data[np.argsort(data[:, 0])]
        wall_time_calc(data, solver,
                 style='{0}-'.format(style_list[counter]))
        counter += 1  # incrementing the counter for style_list


def create_speedup_figure(wildcard, style_list):
    file_names = sorted(glob.glob('*'+wildcard+'*.csv'))

    sort_nicely(file_names)

    plt.title("Speedup for {0}".format(wildcard))

    counter = 0
    for file in file_names:
        # Splitting the name of the file like above
        (atoms, _, _) = file.split('_', 2)
        # Splitting the 20k from the -atoms it is connected to
        atoms = atoms.split('-')[0]
        name = '{0} ({1} atoms)'.format(wildcard, atoms)
        print(name)
        data = np.loadtxt(fname=file, delimiter=',', skiprows=1)
        data = data[np.argsort(data[:, 0])]
        speedup_calc(data, '{0} Atoms'.format(atoms),
                style='{0}-'.format(style_list[counter]))
        counter += 1


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
