# import the necessary packages
import numpy as np
import cv2
import GetCentrePixelPositionOfContour
import config
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
import vision_getandsaveimage
import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
import ALPhotoCapture
import config
import vision_getandsaveimage
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
import Logger
import sys
import math
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot
from Utils import Helper as h

def findObjectOfInterest(InitialiseNaoRobot, filenameTopCamera, filenameBottomCamera):
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
        xCentrePostion = 0
        yCentrePosition = 0
        percentOfImageCoveredWithContour=0

        #SET LOOP VARIABLES
        headDown = False
        headDownChecked = False

        turnCounter = 0


        #check the front first  in case you find the object
        # imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
        print "take first top pic"
        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
        print "initial top cam"
        Logger.Log("initial top cam")
        time.sleep(2)       
        if (xCentrePostion > 0):
            print "OBJECT FOUND"
            Logger.Log("object found")
            print xCentrePostion
            ObjectFound = True
            cameraPosition = 'TOP'
            return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)   
        

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
                xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameBottomCamera + ".png", "BOTTOM",imB)
                if (xCentrePostion > 0):
                    print "OBJECT FOUND"
                    print xCentrePostion
                    cameraPosition = 'BOTTOM'
                    ObjectFound = True
                    print "checking from bottom camera"
                    Logger.Log("bottom cam")
                    print xCentrePostion, yCentrePosition, objectFoundOnBottomCamera,bottomMostPoint
                    h.WalkToPosition(motionProxy, 0.0, 0, math.radians(angleOfHead))
                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    time.sleep(2)
                    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)
                time.sleep(2)
                
                if (xCentrePostion <= 0):
                    #use top camera only if bottom camera cannot see ...
                    # imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
                    imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                    xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
                    print "top cam"
                    Logger.Log("top cam")
                    time.sleep(2)       
                if (xCentrePostion > 0):
                    print "OBJECT FOUND"
                    print xCentrePostion
                    ObjectFound = True
                    cameraPosition = 'TOP'
                    print "top camera values"
                    print xCentrePostion, yCentrePosition, objectFoundOnBottomCamera
                    h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(angleOfHead)*1.5)
                    time.sleep(3)
                    #keep turning until centre of table is mid way
                    # imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
                    # xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
                    # while(xCentrePostion < (config.imageWidth/2)):
                    #     WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, math.radians(20))#20 degrees
                    #     imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
                    # xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 

                    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                    time.sleep(3)
                    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)   
    
                print "values found in this turn"
                print xCentrePostion, yCentrePosition, objectFoundOnBottomCamera

                angleOfHead = angleOfHead - 50
                print "angle of head"
                print angleOfHead
                Logger.Log(str(angleOfHead))
                h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
                time.sleep(2)

            print "out of inner loop"
         
            h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0.0, 0, math.radians(180))
            turnCounter = turnCounter + 1
            time.sleep(4)
            if (turnCounter % 2 == 0):
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 1, 0, 0)
                time.sleep(3)
            
  
    except Exception as e:
        print e
        return (xCentrePostion, yCentrePosition,"", False,0)