from __future__ import division
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

# Description: Assists the robot to perform various actions
def MoveWithObstacleAvoidanceTowardOtherCorner(InitialiseNaoRobot, directionToMoveAway):
    Logger.Log("MoveWithObstacleAvoidance")
    filenameTopCamera = "naoImageTopCamera"
    movedToOtherCorner = False
    objectOutOfSight = False
    moveRatio = 1.0
    previousRatio = 1.0
    angleToTurn = 0.3
    angleOfHead = 0
    while not movedToOtherCorner:
        print "SPINNING TO MOVE AWAY MoveWithObstacleAvoidanceTowardOtherCorner"
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)
        print bottomMostPoint
        print cornerPoints
        if directionToMoveAway == "RIGHT" and bottomMostPoint[0] > 5:
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
            time.sleep(2)
        elif directionToMoveAway == "LEFT" and bottomMostPoint[0] > 0 and bottomMostPoint[0] < 635:
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
            time.sleep(2)
        else:
            movedToOtherCorner = True
    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 4)

    if (directionToMoveAway == "RIGHT"):
        angleOfHead = 100 #100 looking left -100 looking right
    elif (directionToMoveAway == "LEFT"):
        angleOfHead = -100 #100 looking left -100 looking right

    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
    h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
    #keeop walking until table out of sight
    while not objectOutOfSight:
        print "WALKING OUT OF SIGHT"
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)
        if directionToMoveAway == "RIGHT" and bottomMostPoint[0] > 5:
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,1)
        elif directionToMoveAway == "LEFT"and bottomMostPoint[0] > 0 and bottomMostPoint[0] < 635:
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,1)
        else:
            objectOutOfSight = True
    h.HeadInitialise(InitialiseNaoRobot.motionProxy)

    #now face table
    facingTable = False
    while not facingTable:
        print "SPINNING TO MOVE AWAY MoveWithObstacleAvoidanceTowardOtherCorner"
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)
        print bottomMostPoint
        print cornerPoints
        if bottomMostPoint[0] <= 0:
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(45))
        elif bottomMostPoint[0] > (config.imageWidth/2.0 + 50):
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(15))
            time.sleep(2)
        elif bottomMostPoint[0] < (config.imageWidth/2.0 - 50):
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(15))
            time.sleep(2)
        else:
            facingTable = True

def MoveWithObstacleAvoidance(InitialiseNaoRobot, directionToMoveAway):
    Logger.Log("MoveWithObstacleAvoidance")
    filenameTopCamera = "naoImageTopCamera"
    movedAway = False
    objectOutOfSight = False
    moveRatio = 1.0
    previousRatio = 1.0
    angleToTurn = 0.3
    angleOfHead = 0
    while not movedAway:
        print "SPINNING TO MOVE AWAY"
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)
        print bottomMostPoint
        print cornerPoints
        if directionToMoveAway == "RIGHT" and bottomMostPoint[0] > 5:
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(90))
            time.sleep(2)
        elif directionToMoveAway == "LEFT" and bottomMostPoint[0] > 0 and bottomMostPoint[0] < 635:
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(90))
            time.sleep(2)
        else:
            movedAway = True
    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,5)

    if (directionToMoveAway == "RIGHT"):
        angleOfHead = 100 #100 looking left -100 looking right
    elif (directionToMoveAway == "LEFT"):
        angleOfHead = -100 #100 looking left -100 looking right

    h.HeadInitialise(InitialiseNaoRobot.motionProxy)
    h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
    #keeop walking until table out of sight
    while not objectOutOfSight:
        print "WALKING OUT OF SIGHT"
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)
        if directionToMoveAway == "RIGHT" and bottomMostPoint[0] > 5:
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,1)
        elif directionToMoveAway == "LEFT"and bottomMostPoint[0] > 0 and bottomMostPoint[0] < 635:
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,1)
        else:
            objectOutOfSight = True
    h.HeadInitialise(InitialiseNaoRobot.motionProxy)

def FindDirectionOfOtherRobotRelativeToTable(InitialiseNaoRobot):
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    headDown = False
    headDownChecked = False
    turnCounter = 0
    angleOfHead = 100
    objectFound = False
    tableInCentre = False
    xCentrePostion = 0
    tablePositionRelativeToRobot = "NONE"

    while not tableInCentre:
        Logger.Log("Adjust table to centre for FindDirectionOfOtherRobotRelativeToTable")
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        #face the other robot
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, closestPnt, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im, config.colourOfHeadOfNao)   
        if (xCentrePostion < (config.imageWidth/2.0)-50):
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(25))
        elif (xCentrePostion > (config.imageWidth/2.0)+50):
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy,math.radians(25))
        else:
            tableInCentre = True

    while not objectFound:
        angleOfHead = 100
        headDown = False
        headDownChecked = False
        time.sleep(3)
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy,math.radians(29.5))   # move head down to get better view of surroundings
        while (angleOfHead >= -100):  # and headDownChecked == False):
            #check if the bottom camera can see object 
            print "FindDirectionOfOtherRobotRelativeToTable"
            Logger.Log("FindDirectionOfOtherRobotRelativeToTable")
            headLookingPosition = 'CENTRE'
            #use top camera only if bottom camera cannot see ...
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPosRobot, yCntrPosRobot, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT, config.colourOfHeadOfNao) 
            time.sleep(2)       
            if (xCntrPosRobot > 0):
                ObjectFound = True
                h.HeadInitialise(InitialiseNaoRobot.motionProxy)
                im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
                xCentrePostionTable, yCentrePositionTable, objectFoundOnBottomCamera, closestPnt, cornerPoints, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", im)

                #determine of table in front or behind robot
                if yCntrPosRobot > 0 and yCentrePositionTable > 0:
                    if yCntrPosRobot < yCentrePositionTable:
                        tablePositionRelativeToRobot = "INFRONT"
                    elif yCntrPosRobot < yCentrePositionTable:
                        tablePositionRelativeToRobot = "BEHIND"
                if xCntrPosRobot < xCentrePostionTable:
                    Logger.Log("FindDirectionOfOtherRobotRelativeToTable is LEFT")    
                    return "LEFT", xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot
                elif xCntrPosRobot > xCentrePostionTable:
                    Logger.Log("FindDirectionOfOtherRobotRelativeToTable is RIGHT")
                    return "RIGHT", xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot
                else:
                    Logger.Log("FindDirectionOfOtherRobotRelativeToTable is NOT FOUND")
                    # return "NOT FOUND"
            print "angle of head"
            print angleOfHead
            Logger.Log(str(angleOfHead))
            print "values found in this turn"
            print xCntrPosRobot, yCntrPosRobot, objFoundBtmCam, tablePositionRelativeToRobot
            angleOfHead = angleOfHead - 50
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
            time.sleep(2)
        return "NOT FOUND", xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot

def FindDirectionOfOtherRobot(InitialiseNaoRobot):
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    headDown = False
    headDownChecked = False
    turnCounter = 0
    angleOfHead = 100
    objectFound = False

    while not objectFound:
        angleOfHead = 100
        headDown = False
        headDownChecked = False
        time.sleep(3)
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy,math.radians(29.5))   # move head down to get better view of surroundings
        while (angleOfHead >= -100):  # and headDownChecked == False):
            #check if the bottom camera can see object 
            print "FindDirectionOfOtherRobot"
            Logger.Log("FindDirectionOfOtherRobot")
            headLookingPosition = 'CENTRE'
            #use top camera only if bottom camera cannot see ...
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPos, yCntrPos, objFoundBtmCam, botMostPnt,pcntImgCovrd,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT,config.colourOfHeadOfNao) 
            time.sleep(2)       
            if (xCntrPos > 0):
                ObjectFound = True
                if (angleOfHead > 0):
                    Logger.Log("FindDirectionOfOtherRobot is LEFT")
                    return "LEFT"
                elif (angleOfHead < 0):
                    Logger.Log("FindDirectionOfOtherRobot is RIGHT")
                    return "RIGHT"
                else:
                    Logger.Log("FindDirectionOfOtherRobot is AHEAD")
                    return "AHEAD"
            print "angle of head"
            print angleOfHead
            Logger.Log(str(angleOfHead))
            print "values found in this turn"
            print xCntrPos, yCntrPos, objFoundBtmCam
            angleOfHead = angleOfHead - 50
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(angleOfHead))
            time.sleep(2)


def AlignClosestCornerToMiddle(InitialiseNaoRobot, ErrorMargin = 10, cameraName = "TOP"): 
    Logger.Log("AlignClosestCornerToMiddle")
    filenameTopCamera = "naoImageTopCamera"
    alignedToCentre = False
    moveRatio = 1.0
    previousRatio = 1.0
    angleToTurn = 0.3
    while not alignedToCentre:
        im = ip.getImage(InitialiseNaoRobot, cameraName, filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
        print "inside angle align"
        moveRatio = abs(bottomMostPoint[0] - float(config.imageWidth/2))/float(config.imageWidth/2)
        if moveRatio is None or moveRatio == 0  or moveRatio > 1:
            moveRatio = float(previousRatio)/2
        angleToTurn = 0.2 * moveRatio
        # previousRatio = moveRatio
        #check oin middle point in centre of field of view
        if bottomMostPoint[0] < ((config.imageWidth/2)-ErrorMargin):         
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, angleToTurn)
            print "moving left " + str(bottomMostPoint[0])
            im = ip.getImage(InitialiseNaoRobot, cameraName, filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            
        elif (bottomMostPoint[0] > (config.imageWidth/2+ErrorMargin)):                           
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, angleToTurn)
            im = ip.getImage(InitialiseNaoRobot, cameraName, filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
            print "moving right"
            print bottomMostPoint[0]                
            
        else:
            print "aligned"
            alignedToCentre = True
            # return

def FindLongerSideOfTableBySides(InitialiseNaoRobot):
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    AlignClosestCornerToMiddle(InitialiseNaoRobot,5)
    print "FIND LONGER SIDE OF TABLE BY SIDES"
    Logger.Log("FIND LONGER SIDE OF TABLE BY SIDES")
        #GET rect longer side
    fileName = "TablePicToSelectLongerSide" + str(InitialiseNaoRobot.portName)
    imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
    xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt, contourList, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", imT)

    if (contourList[0][1] < contourList[2][1]):
        print "left side is longer FIND LONGER SIDE OF TABLE BY SIDES"
        Logger.Log("left side is longer FIND LONGER SIDE OF TABLE BY SIDES")
        config.InitialLongerSideOfTable=="LEFT"
    else:
        print "RIGHT side is longer FIND LONGER SIDE OF TABLE BY SIDES"
        Logger.Log("RIGHT side is longer FIND LONGER SIDE OF TABLE BY SIDES")
        config.InitialLongerSideOfTable=="RIGHT"

def FindLongerSideOfTable(InitialiseNaoRobot):
    Logger.Log("FindLongerSideOfTable")
    AlignClosestCornerToMiddle(InitialiseNaoRobot,5)
    filenameTopCamera = "naoImageTopCamera"
    filenameBottomCamera = "naoImageBottomCamera"
    fourtyFiveDegreeInRadians = 1
    turnAngle = 30
    names = "HeadYaw"
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
        h.HeadYawMove(InitialiseNaoRobot.motionProxy, math.radians(turnAngle))  #+ve value to look left
        InitialiseNaoRobot.motionProxy.waitUntilMoveIsFinished()
        time.sleep(2) # DO NOT REMOVE: THIS ALLOWS TIME FOR HEAD TO MOVE
        imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt, contourList, bl, br, tl, tr = d.DetectColour(filenameTopCamera + ".png", "", imT)                        
        print bl,br,tl,tr
        Logger.Log("Extreme points left in order bl br tl tr")
        Logger.Log(str(bl))
        Logger.Log(str(br))
        Logger.Log(str(tl))
        Logger.Log(str(tr))
        hypotLeft = math.hypot(abs(abs(contourList[3][0]) - abs(contourList[0][0])), abs(abs(contourList[3][1]) - abs(contourList[0][1]))*1.33)
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
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)            
        Logger.Log("Extreme points right in order bl br tl tr")
        Logger.Log(str(bl))
        Logger.Log(str(br))
        Logger.Log(str(tl))
        Logger.Log(str(tr))
        hypotRight = math.hypot(abs(abs(contourList[2][0]) - abs(contourList[3][0])), abs(abs(contourList[3][1]) - abs(contourList[2][1]))*1.33)
        # hypotRight = math.hypot(abs(abs(contourList[2][0]) - abs(contourList[3][0])), abs(abs(contourList[2][1]) - abs(contourList[3][1]))*1.33)
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


#walk until robot is close enough to lift table
def WalkAheadUntilVeryCloseToCorner(InitialiseNaoRobot, cameraName = "BOTTOM", fileNameCamera = "naoImageBottomCamera"):
        time.sleep(2)
        # h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        print "KEEP WALKING UNTIL VERY CLOSE TO CORNER"
        Logger.Log("KEEP WALKING UNTIL VERY CLOSE TO CORNER")

        #just added this code
        print "move head down"
        headDownCounter = 0
        maxHeadPitchAngle = 29
        currentHeadPitchAngle = 15
        lastCornerPosition = 0
        
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(currentHeadPitchAngle))
        
        objectSeen = False
        while not (objectSeen):
            print "KEEP WALKING UNTIL VERY CLOSE TO CORNER"
            Logger.Log( "KEEP WALKING UNTIL VERY CLOSE TO CORNER")
            im = ip.getImage(InitialiseNaoRobot, cameraName, fileNameCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(fileNameCamera + ".png", "", im)    
            
            try:
                adjustAngle = 0
                if not contourList:
                    print "CANNOT see object from  cam so walk ahead"
                    Logger.Log("countour list is empty")
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                    # if (lastCornerPosition) > float(config.imageWidth)/2.0:
                    #     h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy,0.78) #spin 45 degrees
                    # else:
                    #     h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.78) #spin 45 degrees
                else:
                    Logger.Log("contour details are")
                    Logger.Log(str(contourList))
                    lastCornerPosition = contourList[3][1]
                    if (closestPnt[1] >= float(config.imageHeight)/2.0):  # ( (contourList[4][1] - closestPnt[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                        objectSeen = True 
                        AlignClosestCornerToMiddle(InitialiseNaoRobot,50, cameraName)
                        # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.05)
                        Logger.Log(str(closestPnt))
                        Logger.Log("height of pic: "+str(contourList[4][1]))
                        print "height of pic: "+str(contourList[4][1])
                        print "CLOSE ENOUGH TO CORNER OF TABLE NOW"
                        Logger.Log("CLOSE ENOUGH TO CORNER OF TABLE NOW")
                        return
                    else:
                        #this determines if robot hits table
                        Logger.Log(str(closestPnt))
                        print ">>> bottom most table position is :: "
                        print closestPnt
                        # XValueToWalk = 0.2*(480-closestPnt[1])/480  #((contourList[4][1] - contourList[3][1])/float(contourList[4][1]))
                        h.WalkAheadUntilFinished(motionProxy,0.1) #-ve 45 degrees turn Y/float(8.0)
                    AlignClosestCornerToMiddle(InitialiseNaoRobot,50, cameraName)
                    if (headDownCounter == 0):
                        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
                        headDownCounter += 1
                    
            except Exception as e:
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                #print e

            # h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
            time.sleep(2)

        print "CLOSE ENOUGH TO CORNER OF TABLE NOW"

        #look straight    
        # h.HeadInitialise(InitialiseNaoRobot.motionProxy)


#Align body of robot with table
def AlignBodyHorizontallyWithTable(InitialiseNaoRobot, cameraName = "TOP", fileNameCamera = "naoImageTopCamera", horizontalSearchRange = 5):
    correctionAngle = math.radians(10)
    #look straight    
    # h.HeadInitialise(InitialiseNaoRobot.motionProxy)
    moveRatio = 1.0
    fileName = "TablePicToSelectLongerSide" + str(InitialiseNaoRobot.portName)
    im = ip.getImage(InitialiseNaoRobot, cameraName, fileName)
    xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(fileNameCamera + ".png", "", im)        
    #if bottom most x is less than 450 (i.e you have move further then walk ahead)
    Logger.Log("Keep walking until very close to table")
    # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.4)
    Aligned = False
    while not (Aligned):
        # moveRatio = h.GetMoveRatio(closestPnt[1],config.imageHeight)
        # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, (0.4*moveRatio))
        im = ip.getImage(InitialiseNaoRobot, cameraName, fileName)
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(fileNameCamera + ".png", "", im)
        print "TURNING TO ALIGN TO TABLE USING TOP CAM"
        LeftYPos, MidYPos, RightYPos = d.DetectYPos(im, horizontalSearchRange, xCntrPos)
        print yCntrPos
        print LeftYPos
        print MidYPos
        print RightYPos

        if (LeftYPos <> 0 and RightYPos <> 0 and abs(LeftYPos-RightYPos) <= config.yPointAlignmentErrorMargin):
            print "COMPLETED ** AlignBodyHorizontallyWithTable"
            Logger.Log("COMPLETED ** AlignBodyHorizontallyWithTable")
            Aligned = True
        if LeftYPos == 0 or RightYPos != 0:
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
        elif LeftYPos != 0 or RightYPos == 0:
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 0.1)
        elif LeftYPos == 0 or RightYPos == 0:
            print "One of the vertical positions not found AlignBodyHorizontallyWithTable"
            Logger.Log("One of the vertical positions not found AlignBodyHorizontallyWithTable")
            Aligned = True

        elif LeftYPos <> 0 and RightYPos <> 0:
            if LeftYPos > RightYPos:
                moveRatio = 1 - (RightYPos / float(LeftYPos)) * correctionAngle
            else:
                moveRatio = 1 - (LeftYPos / float(RightYPos)) * correctionAngle
            correctionAngle = correctionAngle * abs(moveRatio)
            if(LeftYPos > RightYPos and (abs(LeftYPos-RightYPos)>config.yPointAlignmentErrorMargin)):
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, correctionAngle)
            elif(LeftYPos <= RightYPos and ((RightYPos-LeftYPos)>config.yPointAlignmentErrorMargin)):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, correctionAngle)

        

def LookLeftAndRightToAlignToMiddleOfTable(InitialiseNaoRobot, camera = "TOP"):
        #ALIGN to centre using top camera
        #aligned
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        aligned = False
        tableInWholeFieldOfView = False
        rightMostX = 0
        leftMostX = 0
        moveRatio = 1
        turnAngle = 45
        spinRatio = 5*almath.TO_RAD

        print "Look straight ahead"
        while not tableInWholeFieldOfView:
            h.HeadYawMove(InitialiseNaoRobot.motionProxy, 0)  #-ve value to look left,     0.5 then 0.7
            time.sleep(1)
            imT = ip.getImage(InitialiseNaoRobot, camera, filenameBottomCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "", imT) 
            print "X CENTRE POSITION"
            print xCntrPos
            if not xCntrPos or not contourList or xCntrPos == 0:
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.2)
            elif(xCntrPos < 300 and contourList[2][0] > 540):
                print "WALK LEFT sideways based on centroid value"
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.5)         
            elif(xCntrPos > 340 and contourList[0][0] < 100):
                print "WALK RIGHT sideways based on centroid value"
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.5) 
            else:
                tableInWholeFieldOfView = True
        time.sleep(2)



        print "LOOK LEFT THEN RIGHT< FIND DIFF AND ADJUST"     
        #LEFT
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(29))
        while not (aligned):
            print "Aligning nao to object for"
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(turnAngle))  #-ve value to look left,     0.5 then 0.7
            time.sleep(4)
            imT = ip.getImage(InitialiseNaoRobot, camera, filenameBottomCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "", imT)    
            
            print "array contour list LEFT"
            if not contourList:
                leftMostX = 0
            else:
                leftMostX = config.imageWidth - contourList[0][0]
                Logger.Log(str(contourList))
            time.sleep(2)

            time.sleep(2)
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(-turnAngle))  #+ve value to look right,     
            time.sleep(4)
            imT = ip.getImage(InitialiseNaoRobot, camera, filenameBottomCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "", imT)    
            print "array contour list RIGHT"
            
            if not contourList:
                rightMostX = 0
            else:
                rightMostX = contourList[2][0] #rightmost point
                Logger.Log(str(contourList))

            print "calculate adjustment"
            X = 0.1
            Y = 0.1#was 0.3

            time.sleep(3)

            print "X VALUES"
            ##IF LEFT MOST X IS 640 THEN WE CANNOT SEE OBJECT 
            #if (leftMostX == 640):
            #    leftMostX = 0
            Logger.Log(">>left most x and right most x points")
            Logger.Log(str(leftMostX))
            Logger.Log(str(rightMostX))
            print leftMostX , rightMostX

            #look ahead
            # h.HeadYawMove(InitialiseNaoRobot.motionProxy, 0)  #-ve value to look left,     0.5 then 0.7
            # time.sleep(1)
            # imT = ip.getImage(InitialiseNaoRobot, camera, filenameBottomCamera)
            # xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "", imT) 
            # if (xCntrPos > 280 and xCntrPos < 360):
            #     aligned = True
            #     return
            if ((leftMostX==0 and rightMostX==0) and (closestPnt[1] < 100 or closestPnt[1] is None)):
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.2)
            else:
                if (leftMostX < rightMostX):
                    #check if left or righmost point is very close to edge
                    if (abs(leftMostX - rightMostX) <= config.leftMostXAndRightMostXAlignTableErrorMargin):
                        # h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0)
                        aligned = True
                    else:
                        h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,Y) #((leftMostX - rightMostX)/contourList[4][1]) * X, 0)  correctionAngle
                        h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                        Logger.Log("too much to left: "+str(leftMostX - rightMostX))
                        print "too much space to left WALKING RIGHT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
                else:
                     if (abs(leftMostX - rightMostX) <= config.leftMostXAndRightMostXAlignTableErrorMargin):
                        # h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, -Y, 0)
                        aligned = True
                     else:
                        h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,Y) #-((rightMostX - leftMostX)/contourList[4][1]) * X, 0)
                        h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                        Logger.Log("too much to right: "+str(leftMostX - rightMostX))
                        print "too much space to right WALKING LEFT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.05)

            time.sleep(3)

#walk until robot is close enough to lift table
def WalkAheadUntilCloseToLift(InitialiseNaoRobot, cameraName = "BOTTOM", fileNameCamera = "naoImageBottomCamera"):
        time.sleep(2)
        filenameCamera = "naoImageBottomCamera"
        # h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        print "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM"
        Logger.Log("KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM")

        #just added this code
        print "move head down"
        maxHeadPitchAngle = 29
        currentHeadPitchAngle = 10
        
        objectSeen = False
        while not (objectSeen):
            print "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM"
            Logger.Log( "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM")
            im = ip.getImage(InitialiseNaoRobot, cameraName, fileNameCamera)
            # im = vision_getandsaveimage.showNaoImageBottomCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.portName], fileNameCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(fileNameCamera + ".png", "", im)  
            
            try:
                adjustAngle = 0.5
                if not contourList:
                    print "CANNOT see object from bottom cam so walk ahead"
                    Logger.Log("countour list is empty")
                    adjustAngle = 0.5
                    if (config.InitialLongerSideOfTable=="RIGHT"):
                        h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, adjustAngle)
                    elif(config.InitialLongerSideOfTable=="LEFT"):
                        h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy,adjustAngle)
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.4)
                else:
                    Logger.Log("Longer side is ")
                    Logger.Log(str(config.InitialLongerSideOfTable))
                    Logger.Log("contour details are")
                    Logger.Log(str(contourList))
                    
                    # if (closestPnt[1] >= config.maxClosestPoint):  # ( (contourList[4][1] - closestPnt[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                    if (closestPnt[1] >= config.maxClosestPoint or contourList[3][1] >= config.maxClosestPoint or contourList[0][1] >= config.maxClosestPoint or contourList[2][1] >= config.maxClosestPoint):  # ( (contourList[4][1] - closestPnt[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                        objectSeen = True
                        Logger.Log(str(closestPnt))
                        Logger.Log("height of pic: "+str(contourList[4][1]))
                        print "height of pic: "+str(contourList[4][1])
                        print "CLOSE ENOUGH TO TABLE NOW"
                        Logger.Log("CLOSE ENOUGH TO TABLE NOW")
                        return
                    else:
                    #     #if space can be seen then adjust
                    #     if (config.InitialLongerSideOfTable=="RIGHT" and contourList[0][0] > 1 and closestPnt[1] < config.maxClosestPoint):
                    #         #calculate angle to turn to correct
                    #         if (contourList[2][0]< 100): # correct angle if pic only seen to the right
                    #             h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, adjustAngle)
                    #         h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.4)
                    #         time.sleep(2)
                    #     elif(config.InitialLongerSideOfTable=="LEFT" and contourList[2][0] < 639 and closestPnt[1] < config.maxClosestPoint):
                    #         if (contourList[0][0]> 100): # correct angle if pic only seen to the right
                    #             h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,adjustAngle)
                    #         h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.4)

                    #         #this determines if robot hits table
                    #         Logger.Log(str(closestPnt))
                    #         print ">>> bottom most table position is :: "
                    #         print closestPnt
                        if (closestPnt[1] <= 0):
                            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                        elif (closestPnt[1] >= 200):
                            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.03)
                        else:
                            XValueToWalk = float(0.06*(480-closestPnt[1]))/float(config.imageHeight)  #((contourList[4][1] - contourList[3][1])/float(contourList[4][1]))
                            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,XValueToWalk) #-ve 45 degrees turn Y/float(8.0)
                        print "bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1])
                        Logger.Log("bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1]))
                        #spin if angle is too far to the left or right
                        # adjustAngle = 0.5
                        # if (contourList[0][0] >= (float(config.imageWidth)/2.0)):                     
                        #     h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, adjustAngle)
                        # if (contourList[2][0] <= (float(config.imageWidth)/2.0)):
                        #     h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, adjustAngle)
                        # if (contourList[0][0] >= 5):                     
                        #     h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,0.1)
                        # if (contourList[2][0] <= (float(config.imageWidth)-5.0)):
                        #     h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy,0.1)


                        # AlignBodyHorizontallyWithTable(InitialiseNaoRobot,"BOTTOM", fileNameCamera)
                    
            except Exception as e:
                print "ERROR so walking ahead"
                print e
                Logger.Log("ERROR so walking ahead")
                Logger.Log(str(e))
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy,0.2)
                 #spin if angle is too far to the left or right
                if (config.InitialLongerSideOfTable=="RIGHT"):
                    adjustAngle = 0.3
                    h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, adjustAngle)
                elif(config.InitialLongerSideOfTable=="LEFT"):
                    adjustAngle = -0.3
                    h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy,adjustAngle)
                #print e

            h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
            time.sleep(2)

        print "CLOSE ENOUGH TO TABLE NOW"

        #look straight    
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)