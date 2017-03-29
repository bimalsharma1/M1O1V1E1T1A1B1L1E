from Utils import DetectColourInImage as d
from Utils import Helper as h
from Utils import ActionHelper as ah
import Logger
import config
import time
import almath # python's wrapping of almath
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot

def AdjustForVCorner(InitialiseNaoRobot): 
    Logger.Log("Adjust to V corner")
    leftMostAlignmentLimit = config.leftMostAlignmentLimit
    rightMostAlignmentLimit = config.rightMostAlignmentLimit

    acceptableError = config.acceptableErrorForVCentre
    alignedToCentre = False
    adjustedToCorner = False

    rightMostXParallelToLeftMostX = 0
    lefttMostXParallelToRightMostX = 0
    diffBtwnBotMostXAndLMostX = 0
    diffBtwnRMostParallelXAndBotMostX = 0
    diffOfXPositions = 0

    diffBtwnBotMostXAndRMostX = 0
    diffBtwnLMostParallelXAndBotMostX = 0
    filenameTopCamera = "naoImageTopCamera"
    x=0.5
    y=0.2
    previousMoveRatio = 1.0
    turnAngle = config.maxTurnAngleForVCentre*almath.TO_RAD
    
# y Use negative for right
# theta Use negative for clockwise
    while not adjustedToCorner:
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   

        if(cornerPoints[0][1] >= cornerPoints[2][1]):    
            #if leftMostY >= rightMostY table is longer //
            Logger.Log("left most y > right most y")
            Logger.Log(str(cornerPoints[0][1]))
            Logger.Log(str(cornerPoints[2][1]))
            rightMostXParallelToLeftMostX = d.DetectXPos(im, cornerPoints[0][1], cornerPoints[3][0], config.imageWidth, colourToDetect = None)
            diffBtwnBotMostXAndLMostX = cornerPoints[3][0]-cornerPoints[0][0]
            diffBtwnRMostParallelXAndBotMostX = rightMostXParallelToLeftMostX-cornerPoints[3][0]
            Logger.Log("calculated dimensions when left most y is greater than rightmost y")
            Logger.Log(str(rightMostXParallelToLeftMostX))
            Logger.Log(str(diffBtwnBotMostXAndLMostX))
            Logger.Log(str(diffBtwnRMostParallelXAndBotMostX))
            diffOfXPositions = abs(diffBtwnBotMostXAndLMostX - diffBtwnRMostParallelXAndBotMostX)
            Logger.Log("calc of diff x for acceptable error")
            Logger.Log(str(diffOfXPositions))
            if (diffOfXPositions <= acceptableError):
                adjustedToCorner = True
                Logger.Log("Adjusted to corner")
                # h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, x)
                return True
            if (diffBtwnBotMostXAndLMostX > diffBtwnRMostParallelXAndBotMostX):
                #turm left
                moveRatio = h.GetMoveRatio(diffBtwnRMostParallelXAndBotMostX,diffBtwnBotMostXAndLMostX)        
                previousMoveRatio = moveRatio
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, moveRatio*turnAngle) #
                print "turning angle left left most y > right most y"
                # time.sleep(4)
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, y)
                # time.sleep(4)
                Logger.Log("walking dimensions LEFT")
                Logger.Log(str(y*moveRatio))
                # Logger.Log(str((diffBtwnBotMostXAndLMostX-diffBtwnRMostParallelXAndBotMostX))/(diffBtwnBotMostXAndLMostX)*turnAngle)
            else:
                #turm right
                moveRatio = h.GetMoveRatio(diffBtwnBotMostXAndLMostX,diffBtwnRMostParallelXAndBotMostX)
                previousMoveRatio = moveRatio
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, moveRatio*turnAngle) #
                print "turning angle right left most y > right most y"
                # time.sleep(4)
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, y) 
                # time.sleep(4)
                Logger.Log("walking dimensions RIGHT")
                Logger.Log(str(-y*moveRatio))
                # Logger.Log(str(-(diffBtwnRMostParallelXAndBotMostX-diffBtwnBotMostXAndLMostX)/(diffBtwnRMostParallelXAndBotMostX)*turnAngle))
        else:
            #table is longer on \\
            lefttMostXParallelToRightMostX = d.DetectXPos(im, cornerPoints[2][1], cornerPoints[3][0], 0, colourToDetect = None)
            diffBtwnBotMostXAndRMostX = cornerPoints[2][0]-cornerPoints[3][0]
            diffBtwnLMostParallelXAndBotMostX = cornerPoints[3][0] - lefttMostXParallelToRightMostX
            Logger.Log("right most y > left most y")
            Logger.Log(str(lefttMostXParallelToRightMostX))
            Logger.Log(str(diffBtwnBotMostXAndRMostX))
            Logger.Log(str(diffBtwnLMostParallelXAndBotMostX))
            diffOfXPositions = abs(diffBtwnLMostParallelXAndBotMostX - diffBtwnBotMostXAndRMostX)
            Logger.Log("diff of X POSITIONS to compare with acceptable error")
            Logger.Log(str(diffOfXPositions))
            if (diffOfXPositions < acceptableError):
                Logger.Log("Adjusted to corner")
                h.WalkAheadUntilFinished(InitialiseNaoRobot.motionProxy, x)
                adjustedToCorner = True
                return True
            if (diffBtwnLMostParallelXAndBotMostX > diffBtwnBotMostXAndRMostX):
                #turn left
                moveRatio = h.GetMoveRatio(diffBtwnBotMostXAndRMostX,diffBtwnLMostParallelXAndBotMostX)
                previousMoveRatio = moveRatio
                h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, moveRatio*turnAngle) #
                print "turning angle left - right most y > left most y"
                # time.sleep(4)
                h.WalkSideWaysRightUntilFinished(InitialiseNaoRobot.motionProxy, y) 
                Logger.Log("walking dimensions LEFT")
                Logger.Log(str(moveRatio*y))
                # Logger.Log(str((diffBtwnLMostParallelXAndBotMostX-diffBtwnBotMostXAndRMostX)/(diffBtwnLMostParallelXAndBotMostX)))
            else:
                #turm right
                print "turning angle right - right most y > left most y"
                moveRatio = h.GetMoveRatio(diffBtwnLMostParallelXAndBotMostX,diffBtwnBotMostXAndRMostX)
                previousMoveRatio = moveRatio
                h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, moveRatio*turnAngle) #
                # time.sleep(4)
                h.WalkSideWaysLeftUntilFinished(InitialiseNaoRobot.motionProxy, y)
                Logger.Log("walking dimensions RIGHT")
                Logger.Log(str(-y*moveRatio))
                # Logger.Log(str(-(diffBtwnBotMostXAndRMostX-diffBtwnLMostParallelXAndBotMostX)/(diffBtwnBotMostXAndRMostX)*turnAngle))
        # ah.AlignClosestCornerToMiddle(InitialiseNaoRobot)
        # alignedToCentre = False
        # while not alignedToCentre:
        #     im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        #     xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)
        #     print "inside angle align"
        #     #check oin middle point in centre of field of view
        #     if bottomMostPoint[0] < leftMostAlignmentLimit:
        #         h.WalkSpinLeftUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD)
        #         print "moving left"
        #         print bottomMostPoint[0]
        #         print leftMostAlignmentLimit
        #         print cornerPoints[3][0]
        #     elif bottomMostPoint[0] > rightMostAlignmentLimit:
        #         h.WalkSpinRightUntilFinished(InitialiseNaoRobot.motionProxy, 5*almath.TO_RAD)
        #         print "moving right"
        #         print bottomMostPoint[0]
        #         print leftMostAlignmentLimit
        #         print cornerPoints[3][0]
        #     else:
        #         print "aligned"
        #         alignedToCentre = True