import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import vision_getandsaveimage
from Utils import DetectColourInImage as d
import InitialiseHeadAndShoulders
from Utils import Helper as h
from Utils import AjustForVCorner as v
import sys
import os
import DetectCornersFast
import Logger
from Utils import ImageProcessing as ip

def MoveToCornerOfObject(InitialiseNaoRobot):
    lastKnownPositionOfObject = ""
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    fourtyFiveDegreeInRadians = 0.9
    alignedToCentre = False
    turnAngle = 0.00
    count = 0
    names = "HeadYaw"
    times      = [1.0]
    isAbsolute = True
    percentOfImageCoveredWithContour=0
    headDownCounter = 0
    leftMostAlignmentLimit = 300
    rightMostAlignmentLimit = 340
    hypotLeft=0
    hypotRight=0
    X=0
    Y = -0.0 # move left or right
    #positive theta is anticlockwise
    Theta = 1 # amount to turn around in radians
    Logger.Log("STARTING behaviourMoveToCornerOfObject")
    print "start moving robot so that bottom most point is in centre of screen"
    objectInCentreScreen = False
    while not (objectInCentreScreen):   
        bottomMostPoint=[0,0]

        #use top camera only if bottom camera cannot see ...
        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",imT)   
        print "bottommost point"
        print bottomMostPoint[1]
        Logger.Log("bottommost point: "+ str(bottomMostPoint[1]))
    
            #move head pitch down by 5degrees each time it gets closer tot he bottom frame
            #DONT FORGET TO RESET IT LATER
            #head pitch can move a max of 29.5 degrees forward
        if (bottomMostPoint[1] > 240 and headDownCounter < 5):
            headDownCounter = headDownCounter + 1
            print "move head down by x degrees"
            Logger.Log("move head down by x degrees")
            # Example showing multiple trajectories
            names      = [ "HeadPitch"]
            angleLists = [10.0*almath.TO_RAD]
            timeLists  = [1.2]
            isAbsolute = True
            InitialiseNaoRobot.motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        if (bottomMostPoint[1] > 450): #was 430
            Logger.Log("starting at corver to ajusr to v corner")
            objectInCentreScreen = v.AdjustForVCorner(InitialiseNaoRobot)
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, X)
            Logger.Log("SETTING BOTTOM POINT TO CENTRE")
            print "SETTING BOTTOM POINT TO CENTRE"
            alignedToCentre = True
            # while not alignedToCentre:
            #     imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            #     xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",imT)   

            #     #check oin middle point in centre of field of view
            #     if bottomMostPoint[0] < config.leftMostAlignmentLimit:
            #         h.WalkSideWaysLeft(InitialiseNaoRobot.motionProxy, 0.2)
            #         print "moving left" + str(bottomMostPoint[0])
            #     elif bottomMostPoint[0] > config.rightMostAlignmentLimit:
            #         h.WalkSideWaysRight(InitialiseNaoRobot.motionProxy, 0.2)
            #         print "moving right" + str(bottomMostPoint[0])
            #     else:
            #         print "End move to corner of object"
            #         Logger.Log("End move to corner of object")
            #         alignedToCentre = True
            if(objectInCentreScreen):
                return

        turnAngle = (320 - bottomMostPoint[0])/float(320.0) * fourtyFiveDegreeInRadians # get appropriate angle to turn
        print "turn angle"
        print turnAngle
        Logger.Log("turn angle:  " + str(turnAngle))    

        if (bottomMostPoint[0] >= leftMostAlignmentLimit and bottomMostPoint[0] <= rightMostAlignmentLimit):             
            X=2  # was 1.5
            print "bottom y point"
            print bottomMostPoint[1]
            X = ((480.0-bottomMostPoint[1])/float(480.0)) * X
            #h.WalkToPosition(motionProxy, X, 0, 0) 
            print "OBJECT IS IN CENTRE, walking toward it"
            print X
            Logger.Log("OBJECT IS IN CENTRE, walking toward it:  "+ str(X))

        if (bottomMostPoint[1] > 420):
            leftMostAlignmentLimit = 310
            rightMostAlignmentLimit = 330
            fourtyFiveDegreeInRadians = 0.5
            X = 0.1
        X = ((480.0-bottomMostPoint[1])/float(480.0)) * X
                           
        print "horizontal pixel position:  ", str(bottomMostPoint[0])
        Logger.Log("bottom most position:  ")
        Logger.Log( str(bottomMostPoint[0]))
        h.WalkToPosition(InitialiseNaoRobot.motionProxy, X, 0, turnAngle)   
        time.sleep(2)
        Logger.Log("ending behaviourMoveToCornerOfObject")