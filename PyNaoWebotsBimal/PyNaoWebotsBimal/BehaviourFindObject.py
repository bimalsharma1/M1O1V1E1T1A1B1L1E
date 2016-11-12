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
import Helper

def behaviourFindObject(motionProxy, portName):      
    #InitialiseHeadAndShoulders.InitialiseHeadAndShoulders(motionProxy,motionProxy1)
    lastKnownPositionOfObject = ""
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    fourtyFiveDegreeInRadians = 1
    turnAngle = 0.00
    count = 0
    names = "HeadYaw"
    times      = [1.0]
    isAbsolute = True
    percentOfImageCoveredWithContour=0
    # width is  640 pixels and height is 480 pixels

    #X=0
    #Y = -0.0 # move left or right
    ##positive theta is anticlockwise
    #Theta = 1 # amount to turn around in radians

    #print "trying to find object"
    #Logger.Log("Behaviour find object STARTING")
    xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint = findObjectOfInterest.findObjectOfInterest(motionProxy, filenameTopCamera,filenameBottomCamera, portName)
    #print "turn head to point straight main"
    #angleLists      = [0]
    #motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

    ##turn in direction where object found
    #if(headLookingPosition=='RIGHT'):
    #    Theta = -1*Theta
    #    print "turning right from main program. Nao found the object to the right"
    #    Logger.Log("turning right from main program. Nao found the object to the right")
    #print "finding finished"
    #Logger.Log("Behaviour find object FINISHED")


