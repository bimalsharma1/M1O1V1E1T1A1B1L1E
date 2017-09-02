import almath
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
from Utils import ActionHelper as a
from Utils import FileIO as fio
from SimpleBehaviours import MoveToOtherSideOfObject as mo
from SimpleBehaviours import MoveAwayFromObject as ma
from SimpleBehaviours import FindObjectOfInterest as f

# Description: Perform behaviour MoveToCornerOfObject

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
    leftMostAlignmentLimit = 310
    rightMostAlignmentLimit = 330
    hypotLeft=0
    hypotRight=0
    moveRatio = 1.0
    X = 1.5
    Y = -0.0 # move left or right
    #positive theta is anticlockwise
    Theta = 1 # amount to turn around in radians
    Logger.Log("STARTING behaviour MoveToCornerOfObject")

    Logger.Log("ALign image to centre")
    print "ALign image to centre"

    #Wait for leader data to be available
    while not h.isLeaderDataAvailable(InitialiseNaoRobot):
        time.sleep(2)
    print "SELECTING LEADER"
    h.SelectLeader(InitialiseNaoRobot)

    #find position of table relative to robot
    directionOfOtherRobot, xCntrPosRobot, xCentrePostionTable, tablePositionRelativeToRobot = a.FindDirectionOfOtherRobotRelativeToTable(InitialiseNaoRobot)
    print "Table relative to robots is"
    print tablePositionRelativeToRobot
    Logger.Log("Table relative to robots is")
    Logger.Log(str(tablePositionRelativeToRobot)) 
    
    #CODE TO EXECUTE WHEN ROBOTS START ON THE SAME SIDE
    if(InitialiseNaoRobot.isLeader != True):#include logic in here to avoid moving to tother side when starting on the same side
        h.CommunicateLeadershipByPuttingRightHandUp(InitialiseNaoRobot.motionProxy)
        if tablePositionRelativeToRobot != "INFRONT": #if table is not in between the robots
            #wait unil other robot moved away
            while not str(fio.ReadFirstLineInFile("otherRobotMovedAway")).strip().lower() == "movedaway":
                print str(fio.ReadFirstLineInFile("otherRobotMovedAway")).strip().lower() == "movedaway"
                print str(fio.ReadFirstLineInFile("otherRobotMovedAway")).lower()
                time.sleep(2) #wait for 2 seconds
    else:
        
        if tablePositionRelativeToRobot != "INFRONT": #if table is not in between the robots
            ma.MoveAwayFromObject(InitialiseNaoRobot)
            Logger.Log(str(tablePositionRelativeToRobot))
        
        while h.GetApprovalToMoveFromLeader(InitialiseNaoRobot) == False:
            time.sleep(5)
        # FindObjectOfInterest
        xCntrPos, yCntrePos, headPos, objFound, btmPnt = f.FindObjectOfInterest(InitialiseNaoRobot, filenameTopCamera,filenameBottomCamera)
        Logger.Log("Assistant robot move to other side")
        # time.sleep(9999999999999999)
        mo.MoveToOtherSideOfObject(InitialiseNaoRobot)
        return True
    
    print "OUT OF SELECTING LEADER AND MOVING AWAY"
    
    print "start moving robot so that bottom most point is in centre of screen"
    objectInCentreScreen = False
    while not objectInCentreScreen:
        bottomMostPoint = [0, 0]

        #use top camera only if bottom camera cannot see ...
        imT = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,percentOfImageCoveredWithContour,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",imT)   
        a.AlignClosestCornerToMiddle(InitialiseNaoRobot, 25)
        print "bottommost point"
        print bottomMostPoint[1]
        Logger.Log("bottommost point: "+ str(bottomMostPoint[1]))

        if (bottomMostPoint[1] > 360): #was 430
            Logger.Log("starting at corver to ajust to v corner")
            names      = [ "HeadPitch"]
            angleLists = [29.5*almath.TO_RAD]
            timeLists  = [1.2]
            isAbsolute = True
            InitialiseNaoRobot.motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
            # objectInCentreScreen = v.AdjustForVCorner(InitialiseNaoRobot)
            objectInCentreScreen = v.AdjustForVCornerByRange(InitialiseNaoRobot)
            
            # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, X)
            Logger.Log("SETTING BOTTOM POINT TO CENTRE")
            print "SETTING BOTTOM POINT TO CENTRE"
            alignedToCentre = True
            if(objectInCentreScreen):
                return
        else:
            #move head pitch down by 5degrees each time it gets closer tot he bottom frame
            #ALWAYS RESET IT LATER
            #head pitch can move a max of 29.5 degrees forward
            if (bottomMostPoint[1] > float(config.imageHeight)/2.0 and headDownCounter < 3):
                headDownCounter = headDownCounter + 1
                print "move head down by x degrees"
                Logger.Log("move head down by x degrees")
                # Example showing multiple trajectories
                names      = [ "HeadPitch"]
                angleLists = [15.0*almath.TO_RAD]
                timeLists  = [1.2]
                isAbsolute = True
                InitialiseNaoRobot.motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

            turnAngle = abs((float(config.imageWidth)/2 - bottomMostPoint[0])/float(float(config.imageWidth)/2) * fourtyFiveDegreeInRadians) # get appropriate angle to turn
            print "turn angle"
            print turnAngle
            Logger.Log("turn angle:  " + str(turnAngle))    

            moveRatio = h.GetMoveRatio(bottomMostPoint[1], config.imageHeight)    #(480.0-bottomMostPoint[1])/float(480.0)
            if (moveRatio < 0.1 or moveRatio is None or moveRatio>1):
                moveRatio = 0.2
            X = (moveRatio * X)
            if (X < 0.2):
                X = 0.2
                            
            print "horizontal pixel position:  ", str(bottomMostPoint[0])
            Logger.Log("bottom most position:  ")
            Logger.Log( str(bottomMostPoint[0]))

            # if bottomMostPoint[0] <= ((config.imageWidth/2)-25):
            #     h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, turnAngle)
            # if bottomMostPoint[0] >= ((config.imageWidth/2)+25):
            #     h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, turnAngle)
            a.AlignClosestCornerToMiddle(InitialiseNaoRobot, 50)
            if (bottomMostPoint[1] > 300):
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, 0.15)
            else:
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, X)
            # h.WalkToPosition(InitialiseNaoRobot.motionProxy, X, 0, turnAngle)
            print "XXXXXXXXXXX WALKING AHEAD XXXXXXXX"
            print X
            
            # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, X)
    time.sleep(2)
    Logger.Log("Walk closer and align again")
    # h.WalkAheadUntilFinished(InitialiseNaoRobot, 0.2)
    Logger.Log("ALign image to centre")
    print "ALign image to centre"
    a.AlignClosestCornerToMiddle(InitialiseNaoRobot, 30)
    Logger.Log("ending behaviourMoveToCornerOfObject")