import os
from datetime import datetime
import Logger

def WriteMessageToFile(InitialiseNaoRobot, msg, fileName):
    EmptyFileContents(fileName+".txt")
    # fileName = "otherRobotMovedAway"
    # robotName = str(InitialiseNaoRobot.ipAddress)+':'+str(InitialiseNaoRobot.portName)
    print str(msg)
    Logger.Log(str(msg))
    # WriteLine(fileName, str(robotName))
    WriteLine(fileName, str(msg))

def WriteLine(filename, stringToWrite):
    # Open a file
    fo = open(filename+".txt",'a') # w for write and a for append
    fo.write(stringToWrite +"\n" );
    # Close opend file
    fo.close()     

def ReadFile(filename):
    f = open(filename, 'r')
    fileContents = f.read()
    f.close()
    return fileContents

def ReadNumLinesInFile(filename):
    counter = 0
    f = open(filename+".txt", 'r')
    Logger.Log("starting count of lines in file")
    # Logger.Log(str(f.read()))
    for line in f:
        counter = counter + 1
        Logger.Log(str(line))
    f.close()
    Logger.Log(str(counter))
    return counter

def ReadFirstLineInFile(filename):
    try:
        counter = 0
        f = open(filename+".txt", 'r')
        message = f.readline()
        Logger.Log(message)
        print "first line of file is :  " + message
        f.close()
        return message
    except:
        return ""

def EmptyFileContents(filename):
    f = open(filename, 'w')
    f.close()






    