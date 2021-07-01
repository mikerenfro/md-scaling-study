import sys

def main():
    analysisTool = sys.argv[1]
    fileNames = sys.argv[2:]
    
    
    if analysisTool == "gromacs":
        gromacsInterpreter(fileNames)
    
    elif analysisTool == "namd":
        namdInterpreter(fileNames)
        
    elif analysisTool == "lammps":
        lammpsInterpreter(fileNames)
        
    else:
        sys.stderr.write("This Analysis Tool is not compatible with this program.")

def gromacsInterpreter(fileNames):
    print("Cores,Time (sec)") #Starting the csv with the header. It is removed later and is more for human readability.
    
    for fileName in fileNames: #Start of the for-loop. It iterates strings that are directories for files.
        nameSplit = fileName.split('/') #Splitting the directories up for naming things later.
        
        coreFinder = nameSplit[0] #Getting the number of cores via taking the directory name and removing useless data.
        
        charIndex = coreFinder.find('atoms') #Finding where to cut off useless data
        
        numCores = coreFinder[charIndex+5:] #Initializing numCores as a String and removing most useless data
        
        numCores = numCores.replace('C', '') #Removing the redundant C, as it is just there to show it is a core number.
        
        readFile = open(fileName, "r") #Opening the file that will have the wallTime that is useful to extract.
        
        #This for-loop iterates through lines of a given log file.
        #It does this to sift through the lines to attempt to find wallTime on each line at the end.
        for line in (readFile.readlines() [-5:]): #This searches the last 5 lines of the log file to find the wallTime
            line = line.strip() #These next two lines simply make searching for Time easier.
            line = line.split()
            
            #This for-loop iterates through the line that has time on it, searching for Time.
            #The reasoning is that the line number the wallTime is on changes from analysis type to analysis type; 
            #therefore this looks for the line it is on via a linear search of every line, provided by the last for-loop
            #It breaks out of the inner most for-loop when it finds what it is looking for and moving on.
            for finder,time in enumerate(line): 
                if time == "Time:": #Trying to find the line with the Time:
                    #The Plus 2 below is to find the word or "column" (depending on how you think of it)
                    wallTime = line[finder+2] #Initializing wallTime as a string, giving it the value of the found number
                    break
        
        print(numCores+","+wallTime) #This prints all of the data every loop into the .csv via the shell script
        readFile.close() #Closing the files

            
def namdInterpreter(fileNames):
    print("Cores,Time (sec)")
    
    for fileName in fileNames:
        nameSplit = fileName.split('/')
        coreFinder = nameSplit[0]
        charIndex = coreFinder.find('atoms')
        numCores = coreFinder[charIndex+5:]
        numCores = numCores.replace('C', '')
        readFile = open(fileName, "r")
        for line in (readFile.readlines() [-2:]):
            line = line.strip()
            line = line.split()
            for finder,time in enumerate(line):
                if time == "CPUTime:":
                    wallTime = line[finder+1]
                    break
        print(numCores+","+wallTime)
        readFile.close()


def lammpsInterpreter(fileNames):
    print("Cores,Time (sec)")
    
    for fileName in fileNames:
        nameSplit = fileName.split('/')
        coreFinder = nameSplit[0]
        charIndex = coreFinder.find('atoms')
        numCores = coreFinder[charIndex+5:]
        numCores = numCores.replace('C', '')
        readFile = open(fileName, "r")
        for line in (readFile.readlines() [-2:]):
            line = line.strip()
            line = line.split()
            for finder,time in enumerate(line):
                if time == "time:":
                    wallTime = line[finder+1]
                    break
                    
        splitTime = wallTime.split(':') #LAMMPS, annoyingly, does its time in hh:mm:ss, so it is split up.
        calcTime = int(splitTime[0])*60**2 + int(splitTime[1])*60 + int(splitTime[2]) #This converts those numbers into seconds.
        wallTime = str(calcTime) #Making the seconds back into a string.
        print(numCores+","+wallTime)
        readFile.close()
    
    
if __name__ == "__main__":
    main()
