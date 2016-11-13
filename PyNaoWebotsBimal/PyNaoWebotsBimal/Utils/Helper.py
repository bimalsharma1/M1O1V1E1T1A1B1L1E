# -*- encoding: UTF-8 -*-
'''Main progrm written by Bimal Sharma to start Nao control'''
import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
import ALPhotoCapture
import config
import vision_getandsaveimage
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
import sys
import findObjectOfInterest
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
    ipList = InitialiseNaoRobot.ipAddress+':'+str(InitialiseNaoRobot.portName)
    # nao = InitialiseNaoRobot.InitialiseNaoRobot
    config.WirelessMessages.append([ipList,0,"New Nao"])
    InitialiseNaoRobot.ListOfNaosDetected.append([ipList,0,"New Nao"])
    print InitialiseNaoRobot.ListOfNaosDetected
    SelectLeader(InitialiseNaoRobot)

def SelectLeader(InitialiseNaoRobot): #get angle in degrees (+ve value to look down, -ve to look up)

    ipList = InitialiseNaoRobot.ipAddress+':'+str(InitialiseNaoRobot.portName)
    leader = max(sublist[0] for sublist in InitialiseNaoRobot.ListOfNaosDetected)
    if (leader == ipList):
        InitialiseNaoRobot.isLeader = True
    print "THE LEADER IS: "
    Logger.Log("THE LEADER IS: ")
    print leader
    Logger.Log(leader)

def SendMessage(ipAddress, port):
    config.ListOfNaosDetected.append([config.ipAddress+str(config.ports['port1']), [MsgReceived], [MsgSent]])

def ReadMessage(ipAddress, port):
    config.ListOfNaosDetected.append([config.ipAddress+str(config.ports['port1']), [MsgReceived], [MsgSent]])

def ReadyToLift():
    for port in config.ports:
        print port