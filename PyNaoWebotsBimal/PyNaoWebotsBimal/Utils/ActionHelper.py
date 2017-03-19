from Utils import DetectColourInImage as d
from Utils import Helper as h
import Logger
import config
import time
import almath # python's wrapping of almath
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot
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
import cv2

def AlignClosestCornerToMiddle(InitialiseNaoRobot, ErrorMargin = 10): 
    filenameTopCamera = "naoImageTopCamera"
    alignedToCentre = False
    moveRatio = 1
    while not alignedToCentre:
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
        print "inside angle align"
        moveRatio = abs(bottomMostPoint[0] - (config.imageWidth/2))/(config.imageWidth/2)
        if moveRatio is None or moveRatio == 0:
            moveRatio = 1
        #check oin middle point in centre of field of view
        if bottomMostPoint[0] < (config.imageWidth/2-ErrorMargin):
            h.WalkSideWaysLeft(InitialiseNaoRobot.motionProxy, 0.2*moveRatio)
            print "moving left " + str(bottomMostPoint[0])
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD*moveRatio)
            print "moving left"
            print bottomMostPoint[0]
            print config.leftMostAlignmentLimit
            print cornerPoints[3][0]
        elif (bottomMostPoint[0] > (config.imageWidth/2+ErrorMargin)):                
            h.WalkSideWaysRight(InitialiseNaoRobot.motionProxy, 0.2*moveRatio)
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            print "moving right"
            print bottomMostPoint[0]                
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD*moveRatio)
            print "moving right"
            print bottomMostPoint[0]
            print config.leftMostAlignmentLimit
            print cornerPoints[3][0]
        else:
            print "aligned"
            alignedToCentre = True

def FindLongerSideOfTable(InitialiseNaoRobot): 
    AlignClosestCornerToMiddle(InitialiseNaoRobot,5)
    lastKnownPositionOfObject = ""
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    fourtyFiveDegreeInRadians = 1
    turnAngle = 30
    names = "HeadYaw"
    times      = [1.0]
    isAbsolute = True
    percentOfImageCoveredWithContour=0
    leftLonger = False
    rightLonger = False
    Y = 1
    correctionAngle = 0.2
    turnAngle = 30
    hypotLeft = 0
    hypotRight = 0
    print "FIND LONGER SIDE OF TABLE"
    Logger.Log("FIND LONGER SIDE OF TABLE")
        #GET rect longer side
    fileName = "TablePicToSelectLongerSide" + str(InitialiseNaoRobot.portName)
    imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
    xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt, contourList, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", imT)

    try:
        #Look LEFT and find length
        Logger.Log("Looking Left")
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(29)) # put blocking call here
        InitialiseNaoRobot.motionProxy.waitUntilMoveIsFinished()
        Logger.Log("Looking Left1")
        h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(turnAngle))  #+ve value to look left
        Logger.Log("Looking Left2")
        InitialiseNaoRobot.motionProxy.waitUntilMoveIsFinished()
        time.sleep(2) # DO NOT REMOVE: THIS ALLOWS TIME FOR HEAD TO MOVE
        imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)                        
        Logger.Log("Looking Left3")
        hypotLeft = math.hypot(abs(abs(contourList[0][0]) - abs(contourList[3][0])), abs(abs(contourList[0][1]) - abs(contourList[3][1])))
        Logger.Log(str(contourList))
        Logger.Log("hypot left " + str(hypotLeft))
    except Exception as e:
        hypotLeft=0
        print "hypot left is 0"
    time.sleep(1)
    try:
        # Look RIGHT and find length
        Logger.Log("Looking Right")
        h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(-1 * turnAngle))  #+ve value to look left,   
        InitialiseNaoRobot.motionProxy.waitUntilMoveIsFinished()
        time.sleep(2) # DO NOT REMOVE: THIS ALLOWS TIME FOR HEAD TO MOVE
        fileName = "ImageRightSide" + str(InitialiseNaoRobot.portName)
        imT = ip.getImage(InitialiseNaoRobot, "TOP" , fileName)
        Logger.Log("Looking Right1")
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)            
        Logger.Log("Looking Right2")
        hypotRight = math.hypot(abs(abs(contourList[2][0]) - abs(contourList[3][0])), abs(abs(contourList[2][1]) - abs(contourList[3][1])))
        Logger.Log(str(contourList))
        Logger.Log("hypot right " + str(hypotRight))
    except Exception as e:
        hypotRight=0
        print "hypot right is 0"    
    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
    time.sleep(2)
    Logger.Log("gypot left ang right values")
    Logger.Log(str(hypotLeft))
    Logger.Log(str(hypotRight))
    if (hypotLeft > hypotRight): # if diff is less than 50 px then it is not accurate):
        print "left side is longer"
        Logger.Log("left side is longer")
        config.InitialLongerSideOfTable=="LEFT"
    else:
        print "right side is longer"
        Logger.Log( "right side is longer")
        config.InitialLongerSideOfTable=="RIGHT"      
    return hypotLeft, hypotRight