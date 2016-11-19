# -*- encoding: UTF-8 -*-
'''Main progrm written by Bimal Sharma to start Nao control'''
import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import vision_getandsaveimage
from Utils import DetectColourInImage
import InitialiseHeadAndShoulders
import sys
import os
import DetectCornersFast
import Logger
import motion
import config
import comms9557
import comms9559

def HeadYawMove(motionProxy, angle): #get angle in degrees (+ve value to turn left, -ve to turn right)
    names = "HeadYaw"   # looking left and right
    times      = [1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)

def HeadPitchMove(motionProxy, angle): #get angle in degrees (+ve value to look down, -ve to look up)
    names = "HeadPitch"   #looking up and down
    times      = [1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)

def HeadInitialise(motionProxy): #straighten up head
    names = "HeadPitch"   #looking up and down
    times      = [1.0]
    isAbsolute = True
    angle = 0
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)   
    names = "HeadYaw"
    motionProxy.angleInterpolation(names, angle, times, isAbsolute)

def LiftWithElbowAndShouldersPutObjectDown(motionProxy):
    #Lshoulder roll goes up to 76 degrees out and LElbow roll goes inwards up tp -88 degrees
    #Rshoulder roll goes up to -76 degrees out and RElbow roll goes inwards up tp 88 degrees
    # Arms motion from user have always the priority than walk arms motion
    #LSHouldPitch goes up by 119 degrees and down by -ve 119 degrees
    pFractionMaxSpeed = 0.02
    
    JointNames = ["LShoulderPitch", "RShoulderPitch"]
    Arm = [70,  70]  #40
    Arm = [ x * motion.TO_RAD for x in Arm]
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm, pFractionMaxSpeed)


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


def AddNao(ipAddress, port): #get angle in degrees (+ve value to look down, -ve to look up)
    ipList = ipAddress+':'+str(port)
    comms9557.ListOfNaosDetected.append([ipList,"",""])
    comms9559.ListOfNaosDetected.append([ipList,"",""])
    SelectLeader(ipAddress, port)

def SelectLeader(ipAddress, port): #get angle in degrees (+ve value to look down, -ve to look up)
    ipList = ipAddress+':'+str(port)
    if(port == 9557):
        config.Leader = max(sublist[0] for sublist in comms9557.ListOfNaosDetected)
    if(port == 9559):
        config.Leader = max(sublist[0] for sublist in comms9559.ListOfNaosDetected)
    print "THE LEADER IS: "
    Logger.Log("THE LEADER IS: ")
    print config.Leader
    Logger.Log(config.Leader)

def SendMessage(ipAddress, port):
    config.ListOfNaosDetected.append([config.ipAddress+str(config.ports['port1']), [MsgReceived], [MsgSent]])

def ReadMessage(ipAddress, port):
    config.ListOfNaosDetected.append([config.ipAddress+str(config.ports['port1']), [MsgReceived], [MsgSent]])

