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
        maxHeadPitchAngle = 29
        Y = 2
        moveRatio = 1
        correctionAngle = 0.3
        # hypotLeft, hypotRight = a.FindLongerSideOfTable(InitialiseNaoRobot)
        a.FindLongerSideOfTableBySides(InitialiseNaoRobot)

        #walk ahead until close enough to lift range
        a.WalkAheadUntilVeryCloseToCorner(InitialiseNaoRobot, "BOTTOM", filenameTopCamera)

        if (config.InitialLongerSideOfTable == "LEFT"):#hypotLeft > hypotRight): # if diff is less than 50 px then it is not accurate
            leftLonger = True
            # config.InitialLongerSideOfTable = "LEFT"
            print "turning angle"
            print math.radians(60)
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75)) #+ve 75 degrees turn
            time.sleep(4)
            print "WALK LEFT DISTANCE"
            print Y
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, Y) #+ve 75 degrees turn

            #adjust and move again
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(40)) #+ve 75 degrees turn
            time.sleep(4)
            print "WALK LEFT DISTANCE"
            print Y
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 0.1) #+ve 75 degrees turn
        else:
            rightLonger = True
            # config.InitialLongerSideOfTable = "RIGHT"
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(75)) #-ve 75 degrees turn 
            time.sleep(4)
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,Y) #-ve 75 degrees turn 
            #adjustand move again
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(40)) #-ve 75 degrees turn 
            time.sleep(4)
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.1) #-ve 75 degrees turn 
        
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
        adjustedToMiddle = False
        print "STARTINg LOOP while not adjustedToMiddle"
        Logger.Log("STARTINg LOOP while not adjustedToMiddle")
        while not adjustedToMiddle:
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   

            if (leftLonger and cornerPoints[2][0] < (float(config.imageWidth)-10)):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.05)
                if (cornerPoints[3][0] < 400):
                    #walk ahead to get close to table
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
            if (rightLonger and cornerPoints[0][0] > 10):
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(10))
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.05)
                if (cornerPoints[3][0] < 400):
                    #walk ahead to get close to table
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
            if((rightLonger and cornerPoints[0][0] <= 10) or (leftLonger and cornerPoints[2][0] >= (float(config.imageWidth)-10))):
                adjustedToMiddle = True
                #this walk will be used for the object to be seen by bottom cam
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                break

        #Look left and right to align to middle of table
        # a.LookLeftAndRightToAlignToMiddleOfTable(InitialiseNaoRobot)

        #Align body of robot with table
        # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"TOP", filenameTopCamera)

        

        #walk ahead until close enough to lift range
        a.WalkAheadUntilCloseToLift(InitialiseNaoRobot)

        #Align body of robot with table
        # a.AlignBodyHorizontallyWithTable(InitialiseNaoRobot, "BOTTOM", filenameBottomCamera)
