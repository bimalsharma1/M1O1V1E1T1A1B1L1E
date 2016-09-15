import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
import Helper
import ALPhotoCapture
import config
import vision_getandsaveimage
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
import WalkToPosition 
import sys
import findObjectOfInterest
import os
import DetectCornersFast
import Logger
import BehaviourMoveTable
import findNaoObjectPositions
import WalkToPosition
import Helper

def LiftObject(motionProxy, portName, X, Y, Theta):
    time.sleep(2)
    readyToLift = findNaoObjectPositions.findIfNaoBehindObject(motionProxy, portName)
    print "ready STATUS"
    print readyToLift

    readyToLift = True

    time.sleep(1)
    Helper.LiftWithElbowAndShoulders(motionProxy)
    if (readyToLift):
        #LIFT WITH ARMS AND SHOULDERS
        time.sleep(1)
        print "move arms"
        WalkToPosition.WalkToPositionWithHandsUp(motionProxy, X, Y, Theta)
        time.sleep(4)
        Helper.LiftWithElbowAndShouldersPutObjectDown(motionProxy)
        time.sleep(3)
        WalkToPosition.WalkToPosition(motionProxy, -2, 0, 0)

def behaviourWalkToLiftRangeOfObject(motionProxy,portName): 
        #InitialiseHeadAndShoulders.InitialiseHeadAndShoulders(motionProxy,motionProxy1)
        lastKnownPositionOfObject = ""
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        fourtyFiveDegreeInRadians = 1
      
        count = 0
        names = "HeadYaw"
        times      = [1.0]
        isAbsolute = True
        percentOfImageCoveredWithContour=0

        #LIFT WITH ARMS AND SHOULDERS
        time.sleep(4)
        print "move arms"
        Helper.LiftWithElbowAndShoulders(motionProxy)

        print "START OF WALK TO RANGE OF OBJECT"
        X=0.05
        print "walk ahead"
        #WalkToPosition.WalkToPosition(motionProxy, X, 0,0) 
        Y = -0.0 # move left or right
        #positive theta is anticlockwise
        Theta = 1 # amount to turn around in radians
        #for y axis, use positive to go to the left
        #ObjectCanBeSeenFromBottomCamera = False
        #while not (ObjectCanBeSeenFromBottomCamera): 
        #    #check if the bottom camera can see object 
        #    print "take pic and walk to LIFT"
        #    imB = vision_getandsaveimage.showNaoImageBottomCam(config.ipAddress, config.ports[portName], filenameBottomCamera)
        #    xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameBottomCamera + ".png", "BOTTOM", imB)
        #    #angleToTurn,distanceToWalk,longerSide = DetectCornersFast.GetTurnAngleAndWalkDistanceWhenCloserToObject(filenameTopCamera + ".png",imB)
        #    print bottomMostPoint
        #    Logger.Log(bottomMostPoint)
        #    #WalkToPosition.WalkToPosition(motionProxy, 0, 0, turnAngle)   
        #    if (bottomMostPoint[1]<460):
        #        WalkToPosition.WalkToPosition(motionProxy, X, 0,0)                     
        #    else:
        #        ObjectCanBeSeenFromBottomCamera=True
        #detect NAO
       

        #print "turn led ON"
        ##Helper.TurnFaceLedsONLeft(motionProxy,portName)
        ## Replace "127.0.0.1" with the IP of your robot
        #leds = ALProxy("ALLeds","127.0.0.1",9559)
        ## Turn the green face LEDs half on
        #leds.setIntensity("LeftFaceLedsGreen", 1)

        



