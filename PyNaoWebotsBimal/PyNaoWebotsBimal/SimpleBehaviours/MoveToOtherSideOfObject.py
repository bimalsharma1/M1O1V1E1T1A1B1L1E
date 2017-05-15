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
from Utils import Helper as h
import math
from Utils import ImageProcessing as ip
from Utils import DetectColourInImage as d
from Utils import PerspectiveTransform as p
from Utils import ActionHelper as a
import cv2

# Description: Perform behaviour MoveToOtherSideOfObject

#contourList[0]    #leftmost
#contourList[1]    #topmost
#contourList[2]    #rightmost
#contourList[3] = closestPnt   #bottomMOst
##contourList[4] HAS HEIGHT AND WIDTH 
# class MoveToOtherSideOfObject:
def MoveToOtherSideOfObject(InitialiseNaoRobot):
        print "START MOVING TO OTHER SIDE MoveToOtherSideOfObject"
        Logger.Log("START MOVING TO OTHER SIDE MoveToOtherSideOfObject") 
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        adjustedToOtherSide = False
        directionToMove = ""
        directionOfOtherRobot = a.FindDirectionOfOtherRobot(InitialiseNaoRobot)
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        if (directionOfOtherRobot == "LEFT"):
            directionToMove = "RIGHT"
            
        elif (directionOfOtherRobot == "RIGHT"):
            directionToMove = "LEFT"
        else:
            return
        print directionToMove
        Logger.Log("DIRECTION TO MOVE IS")
        Logger.Log(str(directionToMove))
        while not adjustedToOtherSide:
            print "MOVING TO OTHER SIDE MoveToOtherSideOfObject"
            im = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, closestPnt,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
            # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM",filenameBottomCamera)
            print "CLOSEST POINT OF MOVING TO OTHER SIDE MoveToOtherSideOfObject FIRST CORNER"
            print cornerPoints
            closestPnt[1]
            
            if closestPnt[1] <= 300:
                if (directionToMove == "LEFT"):
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(15))
                    h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                else:
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(15))
                    h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
            elif (directionToMove == "LEFT"):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
                print "SPINNING AT ANGLE"
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,1)
                if cornerPoints[0][0] > 450:
                    adjustedToOtherSide = True
                    print "SPINNING AT ANGLE"
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(90))   
                    h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                    break
            else:
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
                print "SPINNING AT ANGLE"
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,1)
                if cornerPoints[0][0] < 190:
                    adjustedToOtherSide = True
                    print "SPINNING AT ANGLE"
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                    h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                    break

        adjustedToOtherSideFinal = False
        
        while not adjustedToOtherSideFinal:
            print "MOVING TO OTHER SIDE MoveToOtherSideOfObject FIRST CORNER REACHED MOVING TO SECOND CORNER"
            Logger.Log("MOVING TO OTHER SIDE MoveToOtherSideOfObject FIRST CORNER REACHED MOVING TO SECOND CORNER") 
            im = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera,closestPnt,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
            # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM",filenameBottomCamera)
            print "CLOSEST POINT OF MOVING TO OTHER SIDE MoveToOtherSideOfObject FIRST CORNER REACHED MOVING TO SECOND CORNER"
            print InitialiseNaoRobot.portName
            print cornerPoints
            Logger.Log(str(cornerPoints))
            Logger.Log(str(closestPnt))
            if closestPnt[1] < 300:
                if (directionToMove == "LEFT"):
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                else:
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
            elif (directionToMove == "LEFT"):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.5)
                if cornerPoints[0][0] > 600:
                    adjustedToOtherSideFinal = True
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                    Logger.Log("OTHER SIDE OF TABLE REACHED")
                    print "OTHER SIDE OF TABLE REACHED"
                    break
            else:
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.5)
                if cornerPoints[0][0] < 40:
                    adjustedToOtherSideFinal = True
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                    Logger.Log("OTHER SIDE OF TABLE REACHED")
                    print "OTHER SIDE OF TABLE REACHED"
                    break