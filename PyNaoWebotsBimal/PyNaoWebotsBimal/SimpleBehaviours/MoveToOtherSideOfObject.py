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
        InitialDirectionOfOtherRobot, xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot = a.FindDirectionOfOtherRobotRelativeToTable(InitialiseNaoRobot)
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        tableBehindCounter = 0
        
        print directionToMove
        Logger.Log("DIRECTION TO MOVE IS")
        Logger.Log(str(directionToMove))
        while not adjustedToOtherSide:
            print "MOVING TO OTHER SIDE MoveToOtherSideOfObject"
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, closestPnt,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
            # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM",filenameBottomCamera)
            print "CLOSEST POINT OF MOVING TO OTHER SIDE MoveToOtherSideOfObject"
            print cornerPoints
            closestPnt[1]
            directionOfOtherRobot, xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot = a.FindDirectionOfOtherRobotRelativeToTable(InitialiseNaoRobot)
            if (directionOfOtherRobot == "LEFT"):
                if(cornerPoints[3][1] < 300):
                    h.WalkAheadUntilFinished(InitialiseNaoRobot, 0.4)
                    time.sleep(2)
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                # directionToMove = "RIGHT"       
            elif (directionOfOtherRobot == "RIGHT"):
                if(cornerPoints[3][1] < 300):
                    h.WalkAheadUntilFinished(InitialiseNaoRobot, 0.4)
                    time.sleep(2)
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 1)
                # directionToMove = "LEFT"
            
            # if (not InitialDirectionOfOtherRobot == directionOfOtherRobot) or tablePositionRelativeToRobot > 4:
            if tablePositionRelativeToRobot == "BEHIND":
                # tableBehindCounter+= 1  #increase this counter to allow robot to move sideways to opposite side more times
                adjustedToOtherSide = True
                return