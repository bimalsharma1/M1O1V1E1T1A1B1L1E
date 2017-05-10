# -*- encoding: UTF-8 -*-
'''Main progrm written by Bimal Sharma to start Nao control'''
import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import vision_getandsaveimage
import InitialiseHeadAndShoulders
import sys
import os
import DetectCornersFast
import Logger
import motion
import config
import comms9557
import comms9559
import argparse
import almath as m # python's wrapping of almath
import InitialiseNaoRobot
import FileIO

def HeadYawMove(motionProxy, angle): #get angle in degrees (+ve value to turn left, -ve to turn right)
    names = "HeadYaw"   # looking left and right
    times      = [1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)
    motionProxy.waitUntilMoveIsFinished()

def HeadPitchMove(motionProxy, angle): #get angle in degrees (+ve value to look down, -ve to look up)
    names = "HeadPitch"   #looking up and down
    times      = [1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)
    motionProxy.waitUntilMoveIsFinished()

def HeadInitialise(motionProxy): #straighten up head
    names = "HeadPitch"   #looking up and down
    times      = [1.0]
    isAbsolute = True
    angle = 0
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)   
    motionProxy.waitUntilMoveIsFinished()
    names = "HeadYaw"
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)
    motionProxy.waitUntilMoveIsFinished()

def LiftWithElbowAndShouldersPutObjectDown(motionProxy):
    #Lshoulder roll goes up to 76 degrees out and LElbow roll goes inwards up tp -88 degrees
    #Rshoulder roll goes up to -76 degrees out and RElbow roll goes inwards up tp 88 degrees
    # Arms motion from user have always the priority than walk arms motion
    #LSHouldPitch goes up by 119 degrees and down by -ve 119 degrees
    pFractionMaxSpeed = 0.02
    
    JointNames = ["LShoulderPitch", "RShoulderPitch"]
    Arm = [90,  90]  #40
    Arm = [ x * motion.TO_RAD for x in Arm]
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)
    motionProxy.waitUntilMoveIsFinished()


def LiftWithElbowAndShoulders(motionProxy):
    #Lshoulder roll goes up to 76 degrees out and LElbow roll goes inwards up tp -88 degrees
    #Rshoulder roll goes up to -76 degrees out and RElbow roll goes inwards up tp 88 degrees
    # Arms motion from user have always the priority than walk arms motion
    #LSHouldPitch goes up by 119 degrees and down by -ve 119 degrees
    pFractionMaxSpeed = 0.02
    
    JointNames = ["LShoulderPitch", "RShoulderPitch"]
    Arm = [30,  30]  #-35
    Arm = [ x * motion.TO_RAD for x in Arm]
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)
    motionProxy.waitUntilMoveIsFinished()

def WalkToPositionWithHandsUp(motionProxy, X, Y, Theta):
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.post.moveTo(X, Y, Theta)
    motionProxy.waitUntilMoveIsFinished()

    

def WalkToPosition(motionProxy, X, Y, Theta):
    motionProxy.post.moveTo(X, Y, Theta)
    #motionProxy1.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function
    #motionProxy.waitUntilMoveIsFinished()


def WalkToPositionWaitUntilWalkFinished(motionProxy, X, Y, Theta):
    motionProxy.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()
    
    #JointNames = ["LElbowYaw", "RElbowYaw"]
    #Arm = [35, -35]
    #Arm = [ x * motion.TO_RAD for x in Arm]
    #motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)

    #JointNames = ["LElbowRoll", "RElbowRoll"]
    #Arm = [-88, 88] #88
    #Arm = [ x * motion.TO_RAD for x in Arm]
    #motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)

    #JointNames = ["LShoulderPitch", "RShoulderPitch"]
    #Arm = [-35,  -35]  #-35
    #Arm = [ x * motion.TO_RAD for x in Arm]
    #motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)

    #JointNames = ["LShoulderRoll",  "RShoulderRoll"]
    #Arm = [76, -76] # -76    76
    #Arm = [ x * motion.TO_RAD for x in Arm]
    #motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)

############################################################################################
#####COmms#
# +ve x for front and  -ve x for backwards
# y Use negative for right
# theta Use negative for clockwise

def WalkAheadUntilFinished(motionProxy, X):
    motionProxy.post.moveTo(X, 0, 0)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkBackUntilFinished(motionProxy, X):
    motionProxy.post.moveTo(-X, 0, 0)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkSideWaysLeftUntilFinished(motionProxy, Y):
    print "WALK SIDEWAYS LEFT" + str(Y)
    motionProxy.post.moveTo(0, Y, 0)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkSideWaysRightUntilFinished(motionProxy, Y):
    print "WALK SIDEWAYS RIGHT" + str(-Y)
    motionProxy.post.moveTo(0, -Y, 0)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkSpinLeftUntilFinished(motionProxy, Theta):
    print "SPIN TO LEFT" + str(Theta)
    motionProxy.post.moveTo(0, 0, Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkSpinRightUntilFinished(motionProxy, Theta):
    print "SPIN TO RIGHT" + str(-Theta)
    motionProxy.post.moveTo(0, 0, -Theta)
    # wait is useful because with post moveTo is not blocking function
    motionProxy.waitUntilMoveIsFinished()

def WalkAhead(motionProxy, X):
    motionProxy.post.moveTo(X, 0, 0)

def WalkBack(motionProxy, X):
    motionProxy.post.moveTo(-X, 0, 0)

def WalkSideWaysLeft(motionProxy, Y):
    motionProxy.post.moveTo(0, Y, 0)

def WalkSideWaysRight(motionProxy, Y):
    motionProxy.post.moveTo(0, -Y, 0)

def WalkSpinLeft(motionProxy, Theta):
    motionProxy.post.moveTo(0, 0, Theta)

def WalkSpinRight(motionProxy, Theta):
    motionProxy.post.moveTo(0, 0, -Theta)

def GetMoveRatio(numerator = 1, denominator = None):
    if (denominator is None):
        denominator = numerator
    startRatio = 1.0
    moveRatio = 1.0

    if (denominator <> 0):
        moveRatio = ((abs(denominator) - abs(numerator)) / abs(denominator))
    else:
        moveRatio = startRatio
    #if cannot calculate angle then use maximum turn angle
    if moveRatio is None or moveRatio == 0 or moveRatio > 1:
        moveRatio = float(startRatio)
    # avoid having ratio that is too small
    if (moveRatio < 0.2):
        moveRatio = 0.2
        print "**MOVE RATIO**"
        print moveRatio
    return moveRatio
    

def CommunicateReadyToLift(motionProxy):
    #Lshoulder roll goes up to 76 degrees out and LElbow roll goes inwards up tp -88 degrees
    #Rshoulder roll goes up to -76 degrees out and RElbow roll goes inwards up tp 88 degrees
    # Arms motion from user have always the priority than walk arms motion
    #LSHouldPitch goes up by 119 degrees and down by -ve 119 degrees
    pFractionMaxSpeed = 0.3

    time.sleep(5)
    JointNames = ["RShoulderPitch","RShoulderRoll","RElbowRoll","RElbowYaw","RWristYaw"]                  
    Arm = [-40,-76,88.5,22, 104.5]
    Arm = [ x * motion.TO_RAD for x in Arm]
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)


def AddNao(InitialiseNaoRobot): #get angle in degrees (+ve value to look down, -ve to look up)
    SendMessage(InitialiseNaoRobot, "NEW NAO")
    print "call read msg"
    ReadMessage(InitialiseNaoRobot)
    # SelectLeader(InitialiseNaoRobot)

def SelectLeader(InitialiseNaoRobot): #get angle in degrees (+ve value to look down, -ve to look up)
    filename = "distance.txt"
    with open(filename) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    listOfDistances = [x.strip() for x in content]
    print listOfDistances
    # Logger.Log(listOfDistances)
    if (len(listOfDistances) > 3):
        if (listOfDistances[1] > listOfDistances[3]):
            config.Leader = listOfDistances[0]
        else:
            config.Leader = listOfDistances[2]
        print config.Leader
        Logger.Log(str(config.Leader))
        if(str(InitialiseNaoRobot.ipAddress)+":"+str(InitialiseNaoRobot.portName) in config.Leader):
            InitialiseNaoRobot.isLeader = True
        print "THE LEADER IS: "
        Logger.Log("THE LEADER IS: ")
        print config.Leader
        Logger.Log(config.Leader)

def isLeaderDataAvailable(InitialiseNaoRobot): #get angle in degrees (+ve value to look down, -ve to look up)
    isLeaderDataAvailable = False
    filename = "distance.txt"
    with open(filename) as f:
        content = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    listOfDistances = [x.strip() for x in content]
    print listOfDistances
    print "WAITING FOR LEADER DATA TO BE AVAILABLE"
    if (len(listOfDistances) >= 4):
        isLeaderDataAvailable = True
    return isLeaderDataAvailable 

def SendLeaderMessage(msg):
    filename = "leader"
    FileIO.WriteLine(filename, str(msg))
    Logger.Log("SendLeaderMessage")
    Logger.Log(str(msg))

def CommunicateLeadershipByPuttingRightHandUp(motionProxy):
    #Lshoulder roll goes up to 76 degrees out and LElbow roll goes inwards up tp -88 degrees
    #Rshoulder roll goes up to -76 degrees out and RElbow roll goes inwards up tp 88 degrees
    # Arms motion from user have always the priority than walk arms motion
    #LSHouldPitch goes up by 119 degrees and down by -ve 119 degrees
    pFractionMaxSpeed = 0.02
    
    JointNames = ["LShoulderPitch", "RShoulderPitch"]
    Arm = [0, 119]  #-35
    Arm = [ x * motion.TO_RAD for x in Arm]
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)
    motionProxy.waitUntilMoveIsFinished()

    # time.sleep(3)
    # Arm = [0,0]
    # Arm = [ x * motion.TO_RAD for x in Arm]
    # motionProxy .angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)

def SendDistanceToObjectMessage(InitialiseNaoRobot, msg):
    filename = "distance"
    robotName = str(InitialiseNaoRobot.ipAddress)+':'+str(InitialiseNaoRobot.portName)
    print "send distance message"
    Logger.Log("send distance message")
    FileIO.WriteLine(filename, str(robotName))
    FileIO.WriteLine(filename, str(msg))
    print "SendDistanceToObjectMessage"
    Logger.Log("SendDistanceToObjectMessage")
    Logger.Log(str(msg))

def SendMessage(InitialiseNaoRobot, msg):
    ipList = InitialiseNaoRobot.ipAddress+':'+str(InitialiseNaoRobot.portName)
    config.WirelessMessages.append([ipList,msg])
    InitialiseNaoRobot.ListOfNaosDetected.append([ipList,msg])
    Logger.Log("SendMessage")
    Logger.Log(str(config.WirelessMessages))
    Logger.Log(str(InitialiseNaoRobot.ListOfNaosDetected))

def ReadMessage(InitialiseNaoRobot):
    print "ReadMessage def in helper"
    NaoName = InitialiseNaoRobot.ipAddress+':'+str(InitialiseNaoRobot.portName)
    for message in InitialiseNaoRobot.ListOfNaosDetected:
        Logger.Log("read messages")
        print str(message)
        Logger.Log(str(message))

def SendReadyToLiftMessage(InitialiseNaoRobot, msg):
    ipList = InitialiseNaoRobot.ipAddress+':'+str(InitialiseNaoRobot.portName)
    InitialiseNaoRobot.ReadyToLiftMessages.append([ipList,msg])
    config.WirelessMessages.append([ipList,msg])
    filename = "readyToLift"
    FileIO.WriteLine(filename, str(ipList) + str(msg))
    Logger.Log("SendReadyToLiftMessage")
    Logger.Log(str(config.WirelessMessages))
    Logger.Log(str(InitialiseNaoRobot.ListOfNaosDetected))

def GetReadyToLift(InitialiseNaoRobot):
    counter = 0
    #read all messages
    print "config list"
    # print config.WirelessMessages
    for msg in config.WirelessMessages:
        for message in InitialiseNaoRobot.ReadyToLiftMessages:
            if (message[0] != msg[0]):
                InitialiseNaoRobot.ListOfNaosDetected.append([msg[0], msg[1]])

    for message in InitialiseNaoRobot.ReadyToLiftMessages:
        if (message[1] == "READYTOLIFT"):
            Logger.Log(str(message[1]))
            print message[1]
            counter = counter + 1
    # print counter       
    Logger.Log("GetReadyToLift")
    Logger.Log(str(config.WirelessMessages))
    Logger.Log(str(InitialiseNaoRobot.ListOfNaosDetected))
    Logger.Log(str(counter) + " NAO READYTOLIFT")
    filename = "readyToLift"
    if (FileIO.ReadNumLinesInFile(filename) >= 2):
        return True
        Logger.Log(str("both nao ready to lift"))
        Logger.Log(str(counter))
        # print counter
    else: return False

def GetSideToWalkWithTable(InitialiseNaoRobot): 
    #read from ready to lift file. First line move in one direction and the other match move in another direction
    textToMatch = str(InitialiseNaoRobot.ipAddress) + ":" + str(InitialiseNaoRobot.portName) + "READYTOLIFT"
    Logger.Log(textToMatch)
    filename = "readyToLift"
    firstLineOfFile = FileIO.ReadFirstLineInFile(filename)
    Logger.Log(str(firstLineOfFile))
    if (textToMatch in firstLineOfFile):
        Logger.Log("GetSideToWalkWithTable - TRUE")
        return True
    else:
        Logger.Log("GetSideToWalkWithTable - FALSE")
        return False     