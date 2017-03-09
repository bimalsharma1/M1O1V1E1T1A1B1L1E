from Utils import DetectColourInImage as d
from Utils import Helper as h
import Logger
import config
import time
import almath # python's wrapping of almath
from Utils import ImageProcessing as ip
from Utils import InitialiseNaoRobot
from Utils import Helper as h

def AdjustForVCorner(InitialiseNaoRobot): 
    Logger.Log("Adjust to V corner")
    leftMostAlignmentLimit = 300
    rightMostAlignmentLimit = 340

    acceptableError = 5

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
    y=0.4
    turnAngle = 30*almath.TO_RAD
    #-ve y walks to the right
    #+ve turnangle spins to the left
    while not adjustedToCorner:
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
        
        #check oin middle point in centre of field of view
        # if not (bottomMostPoint[0] >= leftMostAlignmentLimit and bottomMostPoint[0] <= rightMostAlignmentLimit):             
        #     X=2  # was 1.5
        #     print "bottom y point"
        #     print bottomMostPoint[1]
        #     X = ((480.0-bottomMostPoint[1])/float(480.0)) * X

        if(cornerPoints[0][1] >= cornerPoints[2][1]):    
            #if leftMostY >= rightMostY
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
            if (diffOfXPositions < acceptableError):
                adjustedToCorner = True
                Logger.Log("Adjusted to corner")
                return True
            if (diffBtwnBotMostXAndLMostX > diffBtwnRMostParallelXAndBotMostX):
                #turm left
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, 0, -turnAngle) #(diffBtwnBotMostXAndLMostX-diffBtwnRMostParallelXAndBotMostX)/(diffBtwnBotMostXAndLMostX)*
                print "turning angle left left most y > right most y"
                time.sleep(4)
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, -y, 0) 
                time.sleep(4)
                Logger.Log("walking dimensions LEFT")
                Logger.Log(str(y))
                Logger.Log(str((diffBtwnBotMostXAndLMostX-diffBtwnRMostParallelXAndBotMostX)/(diffBtwnBotMostXAndLMostX)*turnAngle))
            else:
                #turm right
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, 0, turnAngle) #(diffBtwnRMostParallelXAndBotMostX-diffBtwnBotMostXAndLMostX)/(diffBtwnRMostParallelXAndBotMostX)*
                print "turning angle right left most y > right most y"
                time.sleep(4)
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, y, 0) 
                time.sleep(4)
                Logger.Log("walking dimensions RIGHT")
                Logger.Log(str(-y))
                Logger.Log(str(-(diffBtwnRMostParallelXAndBotMostX-diffBtwnBotMostXAndLMostX)/(diffBtwnRMostParallelXAndBotMostX)*turnAngle))
        else:
            lefttMostXParallelToRightMostX = d.DetectXPos(im, cornerPoints[2][1], cornerPoints[3][0], 0, colourToDetect = None)
            diffBtwnBotMostXAndRMostX = cornerPoints[2][0]-cornerPoints[3][0]
            diffBtwnLMostParallelXAndBotMostX = cornerPoints[3][0] - lefttMostXParallelToRightMostX
            Logger.Log("right most y > left most y")
            Logger.Log(str(lefttMostXParallelToRightMostX))
            Logger.Log(str(diffBtwnBotMostXAndRMostX))
            Logger.Log(str(diffBtwnLMostParallelXAndBotMostX))
            if (abs(diffBtwnLMostParallelXAndBotMostX - diffBtwnBotMostXAndRMostX) < acceptableError):
                Logger.Log("Adjusted to corner")
                adjustedToCorner = True
                return True
            if(diffBtwnLMostParallelXAndBotMostX > diffBtwnBotMostXAndRMostX):
                #turm left
                #-ve y walks to the right
                #+ve turnangle spins to the left
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, 0, turnAngle) #(diffBtwnLMostParallelXAndBotMostX-diffBtwnBotMostXAndRMostX)/(diffBtwnLMostParallelXAndBotMostX)*
                print "turning angle left - right most y > left most y"
                time.sleep(4)
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, -y, 0) 
                Logger.Log("walking dimensions LEFT")
                Logger.Log(str(y))
                Logger.Log(str((diffBtwnLMostParallelXAndBotMostX-diffBtwnBotMostXAndRMostX)/(diffBtwnLMostParallelXAndBotMostX)*turnAngle))
            else:
                #turm right
                print "turning angle right - right most y > left most y"
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, 0, -turnAngle) #(diffBtwnBotMostXAndRMostX-diffBtwnLMostParallelXAndBotMostX)/(diffBtwnBotMostXAndRMostX)*
                time.sleep(4)
                h.WalkToPositionWaitUntilWalkFinished(InitialiseNaoRobot.motionProxy, 0, y, 0) 
                Logger.Log("walking dimensions RIGHT")
                Logger.Log(str(-y))
                Logger.Log(str(-(diffBtwnBotMostXAndRMostX-diffBtwnLMostParallelXAndBotMostX)/(diffBtwnBotMostXAndRMostX)*turnAngle))