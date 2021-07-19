import sys

def main():
    analysisTool = sys.argv[1] #The first argument which will be the tool
    fileNames = sys.argv[2:] #All of the other files within model size expansion; 
                             #In other words, 20k -> 1 -> data.out, 20k -> 2 -> data.out, 20k -> 4 -> data.out...
    
    acceptableTools = ["gromacs", "namd", "lammps"]
    if analysisTool not in acceptableTools: #This is an error catcher to prevent someone from
                                            #running the script with tools that aren't able to be prcessed.
        sys.stderr.write("This Analysis Tool is not compatible with this program.\n")
        sys.exit(-1)

    print("Cores , Time (sec)") #Starting the csv with the header. It is removed later and is more for human readability.
    
    #The main reason these have to be different is because each of them have different ways of holding onto Time
    #LAMMPS being the most different. NAMD and GROMACS are very similar.
    if analysisTool == "gromacs": #Figures out what interpreter to use based on analysis tool
        gromacsInterpreter(fileNames)
    
    elif analysisTool == "namd":
        namdInterpreter(fileNames)
        
    elif analysisTool == "lammps":
        lammpsInterpreter(fileNames)

def gromacsInterpreter(fileNames):
    for fileName in fileNames: #Start of the for-loop. It iterates strings that are directories for files.

        wallTimeLine = timeFinder(fileName) #Using the fileName from the for-loop, the timeFinder fuction
                                        #can get the string where the wallTime can be extracted.
                                        #Overall, this cuts down on code reusage and makes the code
                                        #easier to understand.
        
        numCores = fileName.split('/')[-2] #Splitting the directories up for naming things later.
                                           #The negative index is due to better consistency with file structure.
                                           #Getting the number of cores via taking the directory name and removing useless data.

        if wallTimeLine != None: #This checks if the previous function failed extracting one data point.
                                 #If it did fail to extract, this is fine. A singular missing data point
                                 #does not make the csv and eventual graph bad.

            wallTime = wallTimeLine.split()[2] #This changes with each function, but it is skipping to the
                                                   #"column" or index that has the wallTime number.
                                                   #This is yet another example of reducing code.
            print(numCores, ',' ,wallTime)


def namdInterpreter(fileNames):
    for fileName in fileNames:
        wallTimeLine = timeFinder(fileName)
        numCores = fileName.split('/')[-2]

        if wallTimeLine != None:
            wallTime = wallTimeLine.split(' ')[4]            
            print(numCores, ',' ,wallTime)

def lammpsInterpreter(fileNames):
    for fileName in fileNames:
        wallTimeLine = timeFinder(fileName)
        numCores = fileName.split('/')[-2]

        if wallTimeLine != None:
            splitTime = wallTimeLine.split(':') #LAMMPS, annoyingly, does its time in hh:mm:ss.
                                                #Therefore, it is split up in order to be processed
            calcTime = int(splitTime[1])*60**2 + int(splitTime[2])*60 + int(splitTime[3]) #This converts those numbers into seconds.
            print(numCores, ',' ,calcTime)

def timeFinder(fileName):
    with open(fileName, "r") as f: #This opens the file sent here for this function
        for line in (f.readlines() [-5:]): #This scans 5 lines backwards through the output file of the Tools
            line = line.strip() #This line is honestly not needed. It is for better human readability during debugging.
            if "ime:" in line: #Finding any instance that could lead to "time"
                return line #Returning that line that has "time" in it.
    return None #This is a failure state, but it allows the code to run regardless.

if __name__ == "__main__":
    main()
