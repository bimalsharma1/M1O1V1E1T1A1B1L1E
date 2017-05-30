# import the necessary packages
import numpy as np
import cv2
import GetCentrePixelPositionOfContour
import config
import InitialiseHeadAndShoulders
import vision_getandsaveimage
import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import vision_getandsaveimage
from Utils import DetectColourInImage
import InitialiseHeadAndShoulders
import Logger
import sys
import math
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot
from Utils import Helper as h
from Utils import DetectColourInImage as d
from SimpleBehaviours import MoveToOtherSideOfObject as mo 

# Description: Perform behaviour FindObjectOfInterest

def FindObjectOfInterest(InitialiseNaoRobot, filenameTopCamera, filenameBottomCamera):
    objectFound = False
    print "FindObjectOfInterest"
    Logger.Log("FindObjectOfInterest")
    try:

        #turn head around to look for object  
        moveLeftAngleInRadians = 1  # approx 60 degrees
        headLookingPosition = 'CENTRE'
        cameraPosition = 'BOTTOM'
        objectPosition = ""
        #set defaults values        
        Y = -0.0 # move left or right
        Theta = 1
        X = 0.0
        xCntrPos = 0
        yCntrPos = 0
        pcntImgCovrd=0
        #SET LOOP VARIABLES
        headDown = False
        headDownChecked = False
        turnCounter = 0
        angleOfHead = 100
        # check the front first  in case you find the object
        print "take first top pic"
        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
        print "initial top cam"
        Logger.Log("initial top cam")
        time.sleep(2)       
        if (xCntrPos > 0):
            print "OBJECT FOUND"
            print str(InitialiseNaoRobot.portName)
            Logger.Log("object found")
            Logger.Log(str(InitialiseNaoRobot.portName))
            print xCntrPos
            # h.SendDistanceToObjectMessage(InitialiseNaoRobot, str(yCntrPos))
            objectFound = True
            cameraPosition = 'TOP'

            #SELCT LEADER
            h.SendDistanceToObjectMessage(InitialiseNaoRobot, str(yCntrPos))
            #     #align to other side of object
            # print "CHeck for leader to move to the other side"
            # print InitialiseNaoRobot.isLeader
            # Logger.Log("CHeck for leader to move to the other side")
            # Logger.Log(str(InitialiseNaoRobot.isLeader))
            # if(InitialiseNaoRobot.isLeader != True):
            #     mo.MoveToOtherSideOfObject(InitialiseNaoRobot)
            return (xCntrPos, yCntrPos, headLookingPosition, objectFound, botMostPnt)   
        

        while not (objectFound):
            angleOfHead = 100
            headDown = False
            headDownChecked = False
            time.sleep(3)
            h.HeadInitialise(InitialiseNaoRobot.motionProxy)
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
            h.HeadPitchMove(InitialiseNaoRobot.motionProxy,math.radians(29.5))   # move head down to get better view of surroundings
            while (angleOfHead >= -100):  # and headDownChecked == False):
                #check if the bottom camera can see object 
                print "checking straight ahead"
                headLookingPosition = 'CENTRE'
                #use top camera only if bottom camera cannot see ...
                imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
                time.sleep(2)       
                if (xCntrPos > 0):
                    print str(InitialiseNaoRobot.portName)
                    Logger.Log(str(InitialiseNaoRobot.portName))
                    print "OBJECT FOUND"
                    print xCntrPos
                    # angleOfHead = -200
                    objectFound = True
                    print "SELECTING LEADER"
                    h.SendDistanceToObjectMessage(InitialiseNaoRobot, str(yCntrPos))
                    cameraPosition = 'TOP'
                    print "top camera values"
                    print xCntrPos, yCntrPos, objFoundBtmCam
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    time.sleep(2) 
                    break
                print "values found in this turn"
                print xCntrPos, yCntrPos, objFoundBtmCam

                angleOfHead = angleOfHead - 50
                print "angle of head"
                print angleOfHead
                Logger.Log(str(angleOfHead))
                h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))

            print "out of inner loop-checking if object found"
            Logger.Log("out of inner loop-checking if object found")
            if(objectFound):
                break
            # h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(180))
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(180))
            turnCounter = turnCounter + 1
            time.sleep(4)
            if (turnCounter % 2 == 0 and turnCounter > 0):
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 1, 0, 0)
                time.sleep(3)

        if (angleOfHead < 0):
            objectPosition = "RIGHT"
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(45))
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
            while(xCntrPos < float(config.imageWidth)/2.00 or xCntrPos == 0):
                print "SPINNING RIGHT in FindObjectOfInterest"
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(45))
                # h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead)*2)#20 degrees
                time.sleep(2)
                imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
                print "Inside align table found to middle"
                if (xCntrPos > float(config.imageWidth)/2.00):
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    h.SendDistanceToObjectMessage(InitialiseNaoRobot, str(yCntrPos))
                    return (xCntrPos, yCntrPos, headLookingPosition, objectFound, botMostPnt)
        elif(angleOfHead > 0):
            objectPosition = "LEFT"
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(45))
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
            while(xCntrPos > float(config.imageWidth)/2.00 or xCntrPos==0):
                print "SPINNING LEFT in FindObjectOfInterest"
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(45))
                # h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead)*2)#20 degrees
                time.sleep(2)
                imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
                print "Inside align table found to middle"
                if (xCntrPos < float(config.imageWidth)/2.00):
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    h.SendDistanceToObjectMessage(InitialiseNaoRobot, str(yCntrPos))
                    return (xCntrPos, yCntrPos, headLookingPosition, objectFound, botMostPnt)
                    # h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead)*2)
                    
  
    except Exception as e:
        print e
        Logger.Log(str(e))
        return (xCntrPos, yCntrPos,"", False,0)