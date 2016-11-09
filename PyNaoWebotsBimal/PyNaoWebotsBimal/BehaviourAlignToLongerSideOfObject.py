import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
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
import Helper
import math

def behaviourAlignToLongerSideOfObject(InitialiseNaoRobot): 
        #InitialiseHeadAndShoulders.InitialiseHeadAndShoulders(motionProxy,motionProxy1)
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
        Y = 2
        correctionAngle = 0


        print "FIND LONGER SIDE OF TABLE"
        Logger.Log("FIND LONGER SIDE OF TABLE")

            #contourList[0]    #leftmost
            #contourList[1]    #topmost
            #contourList[2]    #rightmost
            #contourList[3] = bottomMostPoint   #bottomMOst
            ##contourList[4] HAS HEIGHT AND WIDTH 

        #GET rect longer side
        #imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)     
        #angleToTurn,distanceToWalk,longerSide = DetectCornersFast.GetTurnAngleAndWalkDistanceWhenCloserToObject(filenameTopCamera + ".png", imT)
        #print angleToTurn,distanceToWalk,longerSide
        try:
            #Look LEFT and find length
            Helper.HeadInitialise(InitialiseNaoRobot.motionProxy)
            Helper.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(29)) # put blocking call here
            Helper.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(turnAngle))  #+ve value to look left
            time.sleep(2)
            imT = vision_getandsaveimage.showNaoImageTopCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.PORT], filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT)            
            hypotLeft = math.hypot(abs(abs(contourList[0][0]) - abs(contourList[3][0])), abs(abs(contourList[0][1]) - abs(contourList[3][1])))
            Logger.Log(str(contourList))
            Logger.Log("hypot left " + str(hypotLeft))
        except Exception as e:
            hypotLeft=0
            print "hypot left is 0"
        time.sleep(3)

        try:
            # Look RIGHT and find length
            #Helper.HeadInitialise(motionProxy)
            Helper.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(-1 * turnAngle))  #+ve value to look left,   
            imT = vision_getandsaveimage.showNaoImageTopCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.PORT], filenameTopCamera)
            time.sleep(2)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT)            
            hypotRight = math.hypot(abs(abs(contourList[2][0]) - abs(contourList[3][0])), abs(abs(contourList[2][1]) - abs(contourList[3][1])))
            Logger.Log(str(contourList))
            Logger.Log("hypot right " + str(hypotRight))
        except Exception as e:
            hypotRight=0
            print "hypot right is 0"
        
        Helper.HeadInitialise(InitialiseNaoRobot.motionProxy)
        time.sleep(2)
        #walk ahead closer to table
        WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0.5, 0, 0) #+ve 45 degrees turn
        time.sleep(3)
        
        if (hypotLeft > hypotRight and config.InitialLongerSideOfTable=="LEFT"): # if diff is less than 50 px then it is not accurate
            print "left side is longer"
            Logger.Log("left side is longer")
            leftLonger = True
            WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy, 0,0, -math.radians(85)) #+ve 45 degrees turn
            time.sleep(4)
            WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy, 0,Y, 0) #+ve 45 degrees turn
            time.sleep(3)
            #WalkToPosition.WalkToPosition(motionProxy,0, Y, 0) #+ve 45 degrees turn
        else:
            print "right side is longer"
            Logger.Log( "right side is longer")
            rightLonger = True
            #WalkToPosition.WalkToPosition(motionProxy,0, 0, math.radians(75)) #-ve 45 degrees turn 
            Y = -1 * Y
            WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, 0, math.radians(85)) #-ve 45 degrees turn 
            time.sleep(4)
            WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0) #-ve 45 degrees turn 
            time.sleep(3)            
        #ALIGN to centre using top camera
         #aligned
        aligned = False   
        print "LOOK LEFT THEN RIGHT< FIND DIFF AND ADJUST"     
        #LEFT
        Helper.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(29))
        while not (aligned):
            print "Aligning nao to object for"
            Helper.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(-turnAngle))  #-ve value to look left,     0.5 then 0.7
            time.sleep(2)
            imT = vision_getandsaveimage.showNaoImageTopCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.PORT], filenameTopCamera)
            xCentrePostion, yCentrePosition, maxPossibleAreaOfBottomCameraCovered, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT)    
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
            Helper.HeadYawMove(InitialiseNaoRobot.motionProxy,math.radians(turnAngle))  #+ve value to look right,     
            time.sleep(2)
            imT = vision_getandsaveimage.showNaoImageTopCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.portName], filenameTopCamera)
            xCentrePostion, yCentrePosition, maxPossibleAreaOfBottomCameraCovered, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT)    
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

            print "TURNING TO ALIGN TO TABLE USING TOP CAM"
            if(botLeft > botRight):
                correctionAngle = 0.2
                #WalkToPosition.WalkToPosition(motionProxy,0, 0, 0.2)
            else:
                correctionAngle = -0.2
                #WalkToPosition.WalkToPosition(motionProxy,0, 0, -0.2)

            print "calculate adjustment"
            X = 0.1
            Y = 0.3#was 0.5

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
                WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0.4, 0, 0) 
            else:
                #if (abs(leftMostX - rightMostX) < 5):
                #    aligned = True
                #    WalkToPosition.WalkToPosition(motionProxy,0.1, 0,0)
                #    print "ALIGNED TO OBJECT"
                #    print "LEFT MOST AND RIGHT MOST POINT ARE: "
                #    print leftMostX, rightMostX
                #    Logger.Log("left most and right most points")
                #    Logger.Log(str(leftMostX - rightMostX))
                    
                if (leftMostX < rightMostX):
                    #check if left or righmost point is very close to edge
                    if (config.InitialLongerSideOfTable=="LEFT"):
                        WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0)
                        aligned = True
                    else:
                        WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, -Y, 0) #((leftMostX - rightMostX)/contourList[4][1]) * X, 0)  correctionAngle
                        Logger.Log("too much to left: "+str(leftMostX - rightMostX))
                        print "too much space to left WALKING RIGHT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
                else:
                    if (config.InitialLongerSideOfTable=="RIGHT"):
                        WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, -Y, 0)
                        aligned = True
                    else:
                        WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0, Y, 0) #-((rightMostX - leftMostX)/contourList[4][1]) * X, 0)
                        Logger.Log("too much to right: "+str(leftMostX - rightMostX))
                        print "too much space to right WALKING LEFT: "+str(leftMostX - rightMostX)
                        print "LEFT MOST AND RIGHT MOST POINT ARE: "
                        print leftMostX, rightMostX
            time.sleep(3)

        time.sleep(2)
        Helper.HeadInitialise(InitialiseNaoRobot.motionProxy)
        print "KEEP WALKING UNTIL OBJECT SEEN BY BOTTOM CAM"


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
            imB = vision_getandsaveimage.showNaoImageBottomCam(InitialiseNaoRobot.IP, config.ports[InitialiseNaoRobot.portName], filenameBottomCamera)
            xCentrePostion, yCentrePosition, maxPossibleAreaOfBottomCameraCovered, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameBottomCamera + ".png", "", imB)  
            

            try:
                adjustAngle = 0
                if not contourList:
                    print "CANNOT see object from bottom cam so walk ahead"
                    Logger.Log("countour list is empty")
                    WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0.5, 0, 0)
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
                            WalkToPosition.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0, adjustAngle)
                        WalkToPosition.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, -0.2, 0)
                        time.sleep(2)
                    elif(config.InitialLongerSideOfTable=="LEFT" and contourList[2][0] < 630 and contourList[3][1] < maxClosestPoint):
                        if (contourList[0][0]> 300): # correct angle if pic only seen to the right
                            adjustAngle = -0.5
                            WalkToPosition.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0, adjustAngle)
                        WalkToPosition.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy,0, 0.2, 0)

                    # if (contourList[3][1] >= maxClosestPoint):  # ( (contourList[4][1] - bottomMostPoint[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                    if (bottomMostPoint[1] >= maxClosestPoint):  # ( (contourList[4][1] - bottomMostPoint[1]) < (contourList[4][1] * 0.25)): #(0 is height and 1 is width)
                        objectSeen = True 
                        Logger.Log(str(bottomMostPoint))
                        Logger.Log("height of pic: "+str(contourList[4][1]))
                        print "height of pic: "+str(contourList[4][1])
                    else:
                        #this determines if robot hits table
                        Logger.Log(str(bottomMostPoint))
                        print "bottom most table position is :: "
                        print bottomMostPoint
                        XValueToWalk = 0.2*(480-bottomMostPoint[1])/480  #((contourList[4][1] - contourList[3][1])/float(contourList[4][1]))
                        WalkToPosition.WalkToPosition(motionProxy,XValueToWalk, 0, 0) #-ve 45 degrees turn Y/float(8.0)
                    print "bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1])
                    Logger.Log("bot most yof BOTTOM CA<MERA: "+ str(contourList[3][1]))

            except Exception as e:
                WalkToPosition.WalkToPosition(InitialiseNaoRobot.motionProxy,0.2, 0, 0)
                #print e

            Helper.HeadPitchMove(InitialiseNaoRobot.motionProxy, math.radians(maxHeadPitchAngle))
            time.sleep(2)

        print "CLOSE ENOUGH TO TABLE NOW"

        #look straight    
        Helper.HeadInitialise(InitialiseNaoRobot.motionProxy)

