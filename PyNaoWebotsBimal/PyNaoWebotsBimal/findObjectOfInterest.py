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
import WalkToPosition 
import Logger
import sys
import Helper
import math

def findObjectOfInterest(motionProxy, filenameTopCamera, filenameBottomCamera, portName):
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
        imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
        print "initial top cam"
        Logger.Log("initial top cam")
        time.sleep(2)       
        if (xCentrePostion > 0):
            print "OBJECT FOUND"
            Logger.Log("onject found")
            print xCentrePostion
            ObjectFound = True
            cameraPosition = 'TOP'
            return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)   
        

        while not (objectFound):
            angleOfHead = 100
            headDown = False
            headDownChecked = False
            time.sleep(3)
            Helper.HeadInitialise(motionProxy)
            Helper.HeadYawMove(motionProxy,math.radians(angleOfHead))
            Helper.HeadPitchMove(motionProxy,math.radians(29.5))   # move head down to get better view of surroundings
            while (angleOfHead >= -100):  # and headDownChecked == False):
                #check if the bottom camera can see object 
                print "checking straight ahead"
                headLookingPosition = 'CENTRE'
                imB =  vision_getandsaveimage.showNaoImageBottomCam(config.ipAddress, config.ports[portName], filenameBottomCamera)
                xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameBottomCamera + ".png", "BOTTOM",imB)
                if (xCentrePostion > 0):
                    print "OBJECT FOUND"
                    print xCentrePostion
                    cameraPosition = 'BOTTOM'
                    ObjectFound = True
                    print "checking from bottom camera"
                    Logger.Log("bottom cam")
                    print xCentrePostion, yCentrePosition, objectFoundOnBottomCamera,bottomMostPoint
                    WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, math.radians(angleOfHead))
                    Helper.HeadInitialise(motionProxy)
                    time.sleep(3)
                    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)
                time.sleep(2)
                
                if (xCentrePostion <= 0):
                    #use top camera only if bottom camera cannot see ...
                    imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
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
                    WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, math.radians(angleOfHead))
                    Helper.HeadInitialise(motionProxy)
                    time.sleep(3)
                    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint)   
    
                print "values found in this turn"
                print xCentrePostion, yCentrePosition, objectFoundOnBottomCamera

                angleOfHead = angleOfHead - 50
                print "angle of head"
                print angleOfHead
                Logger.Log(str(angleOfHead))
                Helper.HeadYawMove(motionProxy,math.radians(angleOfHead))

                #if (angleOfHead < -100):
                #    ##move head down, it is point to the right most side
                #    print "turn head down"      
                #    angleOfHead = 100                           
                #    Helper.HeadYawMove(motionProxy,math.radians(angleOfHead))
                #    Logger.Log("Move head 29.5 degrees down, it is facing rightmost")
                    #if (headDown == True):
                    #    headDownChecked = True
                    #else:
                    #    headDown = True
                    #print "angle is less than -100"

            print "out of inner loop"
         
            WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, math.radians(180))
            turnCounter = turnCounter + 1
            time.sleep(4)
            if (turnCounter % 2 == 0):
                WalkToPosition.WalkToPosition(motionProxy, 1, 0, 0)
                time.sleep(3)
            
                # Shake the head from side to side
            ##turn left
            #print "turn head left"
            #Helper.HeadYawMove(motionProxy,math.radians(50))
            #Logger.Log("Move head 50 degrees left")
            ##use top camera only as head is turned ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found top left "
            #    headLookingPosition = "LEFT"
            #    #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)


            #print "turn head left"
            #Helper.HeadYawMove(motionProxy,math.radians(50))
            #Logger.Log("Move head 50 degrees left")
            ##use top camera only as head is turned ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found top left "
            #    headLookingPosition = "LEFT"
            #    #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)


            #print "turn head right"
            #Helper.HeadYawMove(motionProxy,math.radians(-150))
            #Logger.Log("Move head 150 degrees right")
            ##use top camera only as head is turned ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found top right "
            #    headLookingPosition = "RIGHT"
            #    #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)


            #print "turn head right"
            #Helper.HeadYawMove(motionProxy,math.radians(-50))
            #Logger.Log("Move head 50 degrees right")
            ##use top camera only as head is turned ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found top right "
            #    headLookingPosition = "RIGHT"
            #    #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)
         

            ##move head down, it is point to the right most side
            #print "turn head down"
            #Helper.HeadPitchMove(motionProxy,math.radians(29.5))
            #Logger.Log("Move head 29.5 degrees down, it is facing rightmost")
            ##use top camera only as head is turned ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found top right "
            #    headLookingPosition = "RIGHT"
            #    #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)


            #print "turn head right"
            #angleLists      = [-moveLeftAngleInRadians]
            #motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)  #turn head right
            #headLookingPosition = "RIGHT"
            #print "checking right "
            
            #time.sleep(2)
            ##use top camera only if bottom camera cannot see ...
            #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            #xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT) 
            #if (xCentrePostion > 0):
            #    cameraPosition = 'TOP'
            #    ObjectFound = True
            #    print "found right from top camera"
            #    #WalkToPosition.WalkToPosition(motionProxy,motionProxy1, 0.0, 0, -Theta)  
            #    return (xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound,bottomMostPoint)   
            #time.sleep(2)
          
            #print "turn head to point straight"
            #angleLists      = [0]
            #motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)
            #headLookingPosition = "CENTRE"

            ##Theta = 3.14 # set theta = 1 to get a clockwise turn
            #print "object still not found so turning"
            #WalkToPosition.WalkToPosition(motionProxy, 0.0, 0, Theta) 
            #time.sleep(2)
    except Exception as e:
        print e
        return (xCentrePostion, yCentrePosition,"", False,0)