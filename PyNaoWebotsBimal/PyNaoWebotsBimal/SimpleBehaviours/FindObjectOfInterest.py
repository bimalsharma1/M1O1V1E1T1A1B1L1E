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

def FindObjectOfInterest(InitialiseNaoRobot, filenameTopCamera, filenameBottomCamera):
    objectFound = False
    try:        

        #turn head around to look for object  
        moveLeftAngleInRadians = 1  # approx 60 degrees
        headLookingPosition = 'CENTRE'
        cameraPosition = 'BOTTOM'
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


        #check the front first  in case you find the object
        # imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
        print "take first top pic"
        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
        print "initial top cam"
        Logger.Log("initial top cam")
        time.sleep(2)       
        if (xCntrPos > 0):
            print "OBJECT FOUND"
            Logger.Log("object found")
            print xCntrPos
            ObjectFound = True
            cameraPosition = 'TOP'
            return (xCntrPos, yCntrPos, headLookingPosition, ObjectFound, botMostPnt)   
        

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
                # imB =  vision_getandsaveimage.showNaoImageBottomCam(config.ipAddress, config.ports[portName], filenameBottomCamera)
                imB = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameBottomCamera)
                xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "BOTTOM",imB)
                if (xCntrPos > 0):
                    print "OBJECT FOUND"
                    print xCntrPos
                    cameraPosition = 'BOTTOM'
                    ObjectFound = True
                    print "checking from bottom camera"
                    Logger.Log("bottom cam")
                    print xCntrPos, yCntrPos, objFoundBtmCam,botMostPnt
                    h.WalkToPosition(motionProxy, 0.0, 0, math.radians(angleOfHead)*2)
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    time.sleep(2)
                    return (xCntrPos, yCntrPos, headLookingPosition, ObjectFound, botMostPnt)
                time.sleep(2)
                
                if (xCntrPos <= 0):
                    #use top camera only if bottom camera cannot see ...
                    # imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
                    imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                    xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
                    print "top cam"
                    Logger.Log("top cam")
                    time.sleep(2)       
                if (xCntrPos > 0):
                    print "OBJECT FOUND"
                    print xCntrPos
                    ObjectFound = True
                    cameraPosition = 'TOP'
                    print "top camera values"
                    print xCntrPos, yCntrPos, objFoundBtmCam
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead)*2)
                    #keep turning until centre of table is mid way
                    imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                    xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 
                    while(xCntrPos < (config.imageWidth/2)):
                        h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead))#20 degrees
                        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                        xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT) 

                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    return (xCntrPos, yCntrPos, headLookingPosition, ObjectFound, botMostPnt)   
    
                print "values found in this turn"
                print xCntrPos, yCntrPos, objFoundBtmCam

                angleOfHead = angleOfHead - 50
                print "angle of head"
                print angleOfHead
                Logger.Log(str(angleOfHead))
                h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))

            print "out of inner loop"
         
            h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(180))
            turnCounter = turnCounter + 1
            time.sleep(4)
            if (turnCounter % 2 == 0):
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 1, 0, 0)
                time.sleep(3)
            
  
    except Exception as e:
        print e
        return (xCntrPos, yCntrPos,"", False,0)