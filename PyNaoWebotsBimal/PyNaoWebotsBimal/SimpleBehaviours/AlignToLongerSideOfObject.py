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
def AlignToLongerSideOfObject(InitialiseNaoRobot): 
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        fourtyFiveDegreeInRadians = 1
        names = "HeadYaw"
        leftLonger = False
        rightLonger = False
        Y = 1.5
        moveRatio = 1
        correctionAngle = 0.3
        hypotLeft, hypotRight = a.FindLongerSideOfTable(InitialiseNaoRobot)
        if (hypotLeft > hypotRight): # if diff is less than 50 px then it is not accurate
            leftLonger = True
            config.InitialLongerSideOfTable = "LEFT"
            print "turning angle"
            print math.radians(60)
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(60)) #+ve 60 degrees turn
            print "WALK LEFT DISTANCE"
            print Y
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, Y) #+ve 60 degrees turn
        else:
            rightLonger = True
            config.InitialLongerSideOfTable = "LEFT"
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(60)) #-ve 60 degrees turn 
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,Y) #-ve 60 degrees turn 
        
        adjustedToMiddle = False
        while not adjustedToMiddle:
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   

            if (leftLonger and cornerPoints[2][0] > (float(config.imageWidth)-5)):
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(5))
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, float(Y)/2.0 )
                if (cornerPoints[2][0] < 420):
                    #walk ahead to get close to table
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
            elif (rightLonger and cornerPoints[0][0] > 5):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(5))
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, float(Y)/2.0 )
                if (cornerPoints[2][0] < 420):
                    #walk ahead to get close to table
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
            else:
                adjustedToMiddle = True
        

        #Look left and right to align to middle of table
        a.LookLeftAndRightToAlignToMiddleOfTable(InitialiseNaoRobot)

        #Align body of robot with table
        a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"TOP", filenameTopCamera)

        

        #walk ahead until close enough to lift range
        a.WalkAheadUntilCloseToLift(InitialiseNaoRobot)

        #Align body of robot with table
        # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot, "BOTTOM", filenameBottomCamera)
