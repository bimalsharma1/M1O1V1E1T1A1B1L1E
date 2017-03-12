from Utils import DetectColourInImage as d
from Utils import Helper as h
import Logger
import config
import time
import almath # python's wrapping of almath
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot

def AlignClosestCornerToMiddle(InitialiseNaoRobot): 
    filenameTopCamera = "naoImageTopCamera"
    alignedToCentre = False
    while not alignedToCentre:
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
        print "inside angle align"
        #check oin middle point in centre of field of view
        if bottomMostPoint[0] < config.leftMostAlignmentLimit:
            h.WalkSideWaysLeft(InitialiseNaoRobot.motionProxy, 0.2)
            print "moving left" + str(bottomMostPoint[0])
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD)
            print "moving left"
            print bottomMostPoint[0]
            print config.leftMostAlignmentLimit
            print cornerPoints[3][0]
        elif (bottomMostPoint[0] > config.rightMostAlignmentLimit):                
            h.WalkSideWaysRight(InitialiseNaoRobot.motionProxy, 0.2)
            im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            print "moving right"
            print bottomMostPoint[0]                
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD)
            print "moving right"
            print bottomMostPoint[0]
            print config.leftMostAlignmentLimit
            print cornerPoints[3][0]
        else:
            print "aligned"
            alignedToCentre = True