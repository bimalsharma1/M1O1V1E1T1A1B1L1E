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

#contourList[0]    #leftmost
#contourList[1]    #topmost
#contourList[2]    #rightmost
#contourList[3] = closestPnt   #bottomMOst
##contourList[4] HAS HEIGHT AND WIDTH 
# class MoveToOtherSideOfObject:
def MoveToOtherSideOfObject(InitialiseNaoRobot, directionToMove):
        print "START MOVING TO OTHER SIDE MoveToOtherSideOfObject"
        Logger.Log("START MOVING TO OTHER SIDE MoveToOtherSideOfObject") 
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        adjustedToOtherSide = False

        while not adjustedToOtherSide:
            im = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, closestPnt,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
            a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM",filenameBottomCamera)
            if (xCentrePostion > 0):
                if (directionToMove == "LEFT"):
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                    h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                    if (cornerPoints[0][0] > 320):
                        adjustedToOtherSide = True
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                        h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.4)
                        h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
                        break
                else:
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                    h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                    if (cornerPoints[3][0] < 320):
                        adjustedToOtherSide = True
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                        h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.4)
                        h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
                        break
            else:
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)

        adjustedToOtherSideFinal = False

        while not adjustedToOtherSideFinal:
            im = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, closestPnt,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
            a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM",filenameBottomCamera)
            if (xCentrePostion > 0):
                if (directionToMove == "LEFT"):
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                    h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                    if (cornerPoints[0][0] > 320):
                        adjustedToOtherSideFinal = True
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                        h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                        break
                else:
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                    h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                    if (cornerPoints[3][0] < 320):
                        adjustedToOtherSideFinal = True
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                        h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75))
                        break
            else:
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
