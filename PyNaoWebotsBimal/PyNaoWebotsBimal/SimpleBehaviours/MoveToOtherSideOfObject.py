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
            print cornerPoints[3][1]
            Logger.Log(str(cornerPoints[3][1]))
            
            print "Direction of other robot "

            directionOfOtherRobot, xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot = a.FindDirectionOfOtherRobotRelativeToTable(InitialiseNaoRobot)
            print directionOfOtherRobot
            print tablePositionRelativeToRobot
            Logger.Log(str(directionOfOtherRobot))
            Logger.Log(str(tablePositionRelativeToRobot))
            Logger.Log(str(xCntrPosRobot))
            Logger.Log(str(xCentrePostionTable))
            if (directionOfOtherRobot == "LEFT" and InitialDirectionOfOtherRobot == "LEFT"):
                if(cornerPoints[3][1] < 450):
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.4)
                    time.sleep(2)
                print "walk right"
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 1.5)
                # directionToMove = "RIGHT"       
            elif (directionOfOtherRobot == "RIGHT" and InitialDirectionOfOtherRobot == "RIGHT"):
                if(cornerPoints[3][1] < 450):
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.4)
                    time.sleep(2)
                print "walk left"
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 1.5)
            else: # directionOfOtherRobot == "MIDDLE" and tablePositionRelativeToRobot == "INFRONT":
                print directionOfOtherRobot
                print tablePositionRelativeToRobot
                closeToTable = False
                if (InitialDirectionOfOtherRobot == "LEFT"):
                    h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 1.5)
                else:
                    h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 1.5)
                while not closeToTable:
                    print "keep moving while not close to table"
                    Logger.Log("keep moving while not close to table")
                    
                    imB = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)
                    LeftMostX, RightMostX, TopMostY, BottomMostY = d.DetectFourExtremePoints(imB)
                    if BottomMostY > 0:
                        a.AlignObjectToCentreofFieldOfView(InitialiseNaoRobot, "BOTTOM", config.colourOfHeadOfNao)
                        a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot, "BOTTOM", "naoImageBottomCamera", 50)
                    if ((BottomMostY < 300 and BottomMostY > 0) or BottomMostY is None):
                        if BottomMostY is None:
                            a.AlignObjectToCentreofFieldOfView(InitialiseNaoRobot, "TOP", config.colourOfHeadOfNao)
                        h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.15)
                    else:
                        closeToTable = True
                        adjustedToOtherSide = True
                        return