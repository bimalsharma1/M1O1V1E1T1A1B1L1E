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

# Description: Perform behaviour AlignToMiddleOfTable

#contourList[0]    #leftmost
#contourList[1]    #topmost
#contourList[2]    #rightmost
#contourList[3] = closestPnt   #bottomMOst
##contourList[4] HAS HEIGHT AND WIDTH 
class AlignToMiddleOfTable:
    def AlignToMiddleOfTable(self, InitialiseNaoRobot): 
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        fourtyFiveDegreeInRadians = 1
        names = "HeadYaw"
        leftLonger = False
        rightLonger = False
        maxHeadPitchAngle = 29
        Y = 2
        moveRatio = 1
        correctionAngle = 0.3


        #Align body of robot with table
        a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM", filenameBottomCamera, 50)

        #Look left and right to align to middle of table
        a.LookLeftAndRightToAlignToMiddleOfTable(InitialiseNaoRobot, "BOTTOM")

        #Align body of robot with table
        # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM", filenameBottomCamera, 80)

        #walk ahead until close enough to lift range
        a.WalkAheadUntilCloseToLift(InitialiseNaoRobot)

        #Align body of robot with table
        a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot, "BOTTOM", filenameBottomCamera, 100)
