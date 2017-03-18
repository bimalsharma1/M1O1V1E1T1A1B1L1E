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
        Y = 1.5
        moveRatio = 1
        correctionAngle = 0.3
        hypotLeft, hypotRight = a.FindLongerSideOfTable(InitialiseNaoRobot)
        if (hypotLeft > hypotRight): # if diff is less than 50 px then it is not accurate
            leftLonger = True
            print "turning angle"
            print math.radians(60)
            h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(60)) #+ve 60 degrees turn
            print "WALK LEFT DISTANCE"
            print Y
            h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, Y) #+ve 60 degrees turn
        else:
            rightLonger = True
            h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, math.radians(60)) #-ve 60 degrees turn 
            h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy,Y) #-ve 60 degrees turn 
          
        fileName = "TablePicToSelectLongerSide" + str(InitialiseNaoRobot.portName)
        imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
        xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)        
        #if bottom most x is less than 450 (i.e you have move further then walk ahead)
        Logger.Log("Keep walking until very close to table")
        # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.4)
        while not (closestPnt[1] > 450):
            moveRatio = abs(closestPnt[1]-450)/450
            h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, (0.4*moveRatio))
            imT = ip.getImage(InitialiseNaoRobot, "TOP", fileName)
            xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)
            
            print "TURNING TO ALIGN TO TABLE USING TOP CAM"
            LeftYPos, MidYPos, RightYPos = d.DetectYPos(imT, yCntrPos)
            print yCntrPos
            print LeftYPos
            print MidYPos
            print RightYPos
            #error margin
            if(LeftYPos > RightYPos and ((LeftYPos-RightYPos)>config.yPointAlignmentErrorMargin)):
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, correctionAngle)
                #h.WalkToPosition(motionProxy,0, 0, 0.2)
            elif(LeftYPos <= RightYPos and ((RightYPos-LeftYPos)>config.yPointAlignmentErrorMargin)):
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, correctionAngle)
                #h.WalkToPosition(motionProxy,0, 0, -0.2)
            #align to centroid
            if (xCntrPos<(config.imageWidth/2)):
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, 0.4*moveRatio)
            else:
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, 0.4*moveRatio)

        #ALIGN to centre using top camera
        #aligned
        aligned = False   
        print "LOOK LEFT THEN RIGHT< FIND DIFF AND ADJUST"     
        #LEFT
        h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(29))
        while not (aligned):
            print "Aligning nao to object for"
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(-turnAngle))  #-ve value to look left,     0.5 then 0.7
            time.sleep(2)
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)    
            
            print "array contour list LEFT"
            if not contourList:
                leftMostX = 0
            else:
                leftMostX = 640 - contourList[0][0]
                Logger.Log(str(contourList))
            time.sleep(2)
            print "array bot left"
            try:
                if not bl:
                    botLeft = 0
                else:
                    botLeft = bl[1]
            except Exception as e:
                botLeft = 0

            time.sleep(2)
            h.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(turnAngle))  #+ve value to look right,     
            time.sleep(2)
            imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "", imT)    
            print "array contour list RIGHT"
            
            if not contourList:
                rightMostX = 0
            else:
                rightMostX = contourList[2][0] #rightmost point
                Logger.Log(str(contourList))
            try:
                print "array br"          
                if not br:
                    botRight = 0
                else:
                    botRight = br[1]
            except Exception as e:
                botRight = 0

            print "calculate adjustment"
            X = 0.1
            Y = 0.5#was 0.3

            time.sleep(3)

            print "X VALUES"
            ##IF LEFT MOST X IS 640 THEN WE CANNOT SEE OBJECT 
            #if (leftMostX == 640):
            #    leftMostX = 0
            Logger.Log("left most x and right most x points")
            Logger.Log(str(leftMostX))
            Logger.Log(str(rightMostX))
            print leftMostX , rightMostX
            
            if (leftMostX==0 and rightMostX==0):
                h.WalkToPosition(InitialiseNaoRobot.motionProxy,0.4, 0, 0) 
            else:
                if (leftMostX < rightMostX):
                    #check if left or righmost point is very close to edge
                    if (config.InitialLongerSideOfTable=="LEFT"):
                        h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0)
                        aligned = True
                    else:
                        h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, -Y, 0) #((leftMostX - rightMostX)/contourList[4][1]) * X, 0)  correctionAngle
                        Logger.Log("too much to left: "+str(leftMostX - rightMostX))
                        print "too much space to left WALKING RIGHT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
                else:
                    if (config.InitialLongerSideOfTable=="RIGHT"):
                        h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, -Y, 0)
                        aligned = True
                    else:
                        h.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0) #-((rightMostX - leftMostX)/contourList[4][1]) * X, 0)
                        Logger.Log("too much to right: "+str(leftMostX - rightMostX))
                        print "too much space to right WALKING LEFT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
                if closestPnt[1] < 450:
                    h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.3)

            time.sleep(3)

        time.sleep(2)
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)
        print "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM"
        Logger.Log("KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM")

        #just added this code
        print "move head down"
        maxHeadPitchAngle = 29
        currentHeadPitchAngle = 10
        
        maxClosestPoint = 330
        objectSeen = False
        while not (objectSeen):
            print "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM"
            Logger.Log( "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM")
            time.sleep(2)
            imB = ip.getImage(InitialiseNaoRobot, "BOTTOM", filenameBottomCamera)
            # imB = vision_getandsaveimage.showNaoImageBottomCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.portName], filenameBottomCamera)
            xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(filenameBottomCamera + ".png", "", imB)  
            

            try:
                adjustAngle = 0
                if not contourList:
                    print "CANNOT see object from bottom cam so walk ahead"
                    Logger.Log("countour list is empty")
                    h.WalkToPosition(InitialiseNaoRobot.motionProxy,0.5, 0, 0)
                else:
                    Logger.Log("Longer side is ")
                    Logger.Log(str(config.InitialLongerSideOfTable))
                    Logger.Log("contour details are")
                    Logger.Log(str(contourList))
                    #if space can be seen then adjust
                    if (config.InitialLongerSideOfTable=="RIGHT" and contourList[0][0] > 10 and contourList[3][1] < maxClosestPoint):
                        #calculate angle to turn to correct
                        if (contourList[2][0]< 300): # correct angle if pic only seen to the right
                            adjustAngle = 0.5
                            h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0, adjustAngle)
                        h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, -0.2, 0)
                        time.sleep(2)
                    elif(config.InitialLongerSideOfTable=="LEFT" and contourList[2][0] < 630 and contourList[3][1] < maxClosestPoint):
                        if (contourList[0][0]> 300): # correct angle if pic only seen to the right
                            adjustAngle = -0.5
                            h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0, adjustAngle)
                        h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0.2, 0)

                    # if (contourList[3][1] >= maxClosestPoint):  # ( (contourList[4][1] - closestPnt[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                    if (closestPnt[1] >= maxClosestPoint):  # ( (contourList[4][1] - closestPnt[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                        objectSeen = True 
                        Logger.Log(str(closestPnt))
                        Logger.Log("height of pic: "+str(contourList[4][1]))
                        print "height of pic: "+str(contourList[4][1])
                    else:
                        #this determines if robot hits table
                        Logger.Log(str(closestPnt))
                        print "bottom most table position is :: "
                        print closestPnt
                        XValueToWalk = 0.2*(480-closestPnt[1])/480  #((contourList[4][1] - contourList[3][1])/float(contourList[4][1]))
                        h.WalkToPosition(motionProxy,XValueToWalk, 0, 0) #-ve 45 degrees turn Y/float(8.0)
                    print "bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1])
                    Logger.Log("bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1]))

            except Exception as e:
                h.WalkToPosition(InitialiseNaoRobot.motionProxy,0.2, 0, 0)
                #print e

            h.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
            time.sleep(2)

        print "CLOSE ENOUGH TO TABLE NOW"

        #look straight    
        h.HeadInitialise(InitialiseNaoRobot.motionProxy)

