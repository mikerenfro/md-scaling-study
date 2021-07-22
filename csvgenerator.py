import sys


def main():
    # The first argument which will be the tool
    analysis_tool = sys.argv[1]
    # All of the other files within model size expansion;
    # In other words,
    # 20k -> 1 -> data.out, 20k -> 2 -> data.out, 20k -> 4 -> data.out...
    file_names = sys.argv[2:]

    acceptable_tools = ["gromacs", "namd", "lammps"]

    # This is an error catcher to prevent someone from
    # running the script with tools that aren't able to be prcessed.
    if analysis_tool not in acceptable_tools:
        sys.stderr.write(
            "This Analysis Tool is not compatible with this program.\n"
        )
        sys.exit(-1)

    # Starting the csv with the header.
    # It is removed later and is more for human readability.
    print("Cores , Time (sec)")

    # The main reason these have to be different is because
    # each of them have different ways of holding onto Time
    # LAMMPS being the most different. NAMD and GROMACS are very similar.

    # Figures out what interpreter to use based on analysis tool
    if analysis_tool == "gromacs":
        gromacs_interpreter(file_names)

    elif analysis_tool == "namd":
        namd_interpreter(file_names)

    elif analysis_tool == "lammps":
        lammps_interpreter(file_names)


def gromacs_interpreter(file_names):
    # Start of the for-loop.
    # It iterates strings that are directories for files.
    for file in file_names:
        # Using the file from the for-loop,
        # the time_finder fuction can get
        # the string where the wall_time can be extracted.
        # Overall, this cuts down on code reusage
        # and makes the code easier to understand.
        wall_time_line = time_finder(file)

        # Splitting the directories up for naming things later.
        # The negative index is due to
        # better consistency with file structure.
        # Getting the number of cores via
        # taking the directory name and removing useless data.
        num_cores = file.split('/')[-2]

        # This checks if the previous function
        # failed extracting one data point.
        # If it did fail to extract, this is fine.
        # A singular missing data point
        # does not make the csv and eventual graph bad.
        if wall_time_line is not None:
            # This changes with each function,
            # but it is skipping to the
            # "column" or index that has the wall_time number.
            # This is yet another example of reducing code.
            wall_time = wall_time_line.split()[2]
            # Again, all printed output is normally
            # directly redirects into a csv
            print(num_cores, ',', wall_time)


def namd_interpreter(file_names):
    for file in file_names:
        wall_time_line = time_finder(file)
        num_cores = file.split('/')[-2]

        if wall_time_line is not None:
            wall_time = wall_time_line.split(' ')[4]
            print(num_cores, ',', wall_time)


def lammps_interpreter(file_names):
    for file in file_names:
        wall_time_line = time_finder(file)
        num_cores = file.split('/')[-2]

        if wall_time_line is not None:
            # LAMMPS, annoyingly, does its time in hh:mm:ss.
            # Therefore, it is split up in order to be processed
            [hours, minutes, seconds] = wall_time_line.split(':')
            # This converts those numbers into seconds.
            calc_time = int(hours)*60**2 + int(minutes)*60 + int(seconds)
            print(num_cores, ',', calc_time)


def time_finder(file):
    # This opens the file sent here for this function
    with open(file, "r") as f:
        # This scans 5 lines backwards through
        # the output file of the Tools
        for line in (f.readlines()[-5:]):
            # This line is honestly not needed.
            # It is for better human readability during debugging
            line = line.strip()
            # Finding any instance that could lead to "time"
            if "ime:" in line:
                # Returning that line that has "time" in it.
                return line
    # This is a failure state,
    # but it allows the code to run regardless.
    return None


if __name__ == "__main__":
    main()
