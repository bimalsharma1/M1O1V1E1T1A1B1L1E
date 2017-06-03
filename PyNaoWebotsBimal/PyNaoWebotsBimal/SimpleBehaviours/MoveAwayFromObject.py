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
from Utils import FileIO as fio
import cv2

# Description: Perform behaviour MoveAwayFromObject

#contourList[0]    #leftmost
#contourList[1]    #topmost
#contourList[2]    #rightmost
#contourList[3] = closestPnt   #bottomMOst
##contourList[4] HAS HEIGHT AND WIDTH 
# class MoveToOtherSideOfObject:
def MoveAwayFromObject(InitialiseNaoRobot):
    print "START MoveAwayFromObject"
    Logger.Log("START MoveAwayFromObject") 
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    movedAway = False
    directionToMove = ""
    directionOfOtherRobot = a.FindDirectionOfOtherRobot(InitialiseNaoRobot)
    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
    if (directionOfOtherRobot == "LEFT"):
        a.MoveWithObstacleAvoidance(InitialiseNaoRobot, "RIGHT")
        #send message that other robot has moved away
        fio.WriteMessageToFile(InitialiseNaoRobot, "MovedAway","otherRobotMovedAway")
    elif (directionOfOtherRobot == "RIGHT"):
        a.MoveWithObstacleAvoidance(InitialiseNaoRobot, "LEFT")
        #send message that other robot has moved away
        fio.WriteMessageToFile(InitialiseNaoRobot, "MovedAway","otherRobotMovedAway")
    else:
        return