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

    acceptableError = 20

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
    y=0.5
    turnAngle = 5*almath.TO_RAD

    while not adjustedToCorner:
        im = ip.getImage(InitialiseNaoRobot, "TOP", filenameTopCamera)
        xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,cornerPoints,bl,br,tl,tr = d.DetectColour(filenameTopCamera + ".png", "",im)   
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
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, 0, -(diffBtwnBotMostXAndLMostX-diffBtwnRMostParallelXAndBotMostX)/(diffBtwnBotMostXAndLMostX)*turnAngle) 
                time.sleep(4)
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, y, 0) 
                Logger.Log("walking dimensions")
                Logger.Log(str(y))
                Logger.Log(str((diffBtwnBotMostXAndLMostX-diffBtwnRMostParallelXAndBotMostX)/(diffBtwnBotMostXAndLMostX)*turnAngle))
            else:
                #turm right
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, 0, (diffBtwnRMostParallelXAndBotMostX-diffBtwnBotMostXAndLMostX)/(diffBtwnRMostParallelXAndBotMostX)*turnAngle) 
                time.sleep(4)
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, -y, 0) 
                Logger.Log("walking dimensions")
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
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, 0, -(diffBtwnLMostParallelXAndBotMostX-diffBtwnBotMostXAndRMostX)/(diffBtwnLMostParallelXAndBotMostX)*turnAngle) 
                time.sleep(4)
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, -y, 0) 
                Logger.Log("walking dimensions")
                Logger.Log(str(y))
                Logger.Log(str((diffBtwnLMostParallelXAndBotMostX-diffBtwnBotMostXAndRMostX)/(diffBtwnLMostParallelXAndBotMostX)*turnAngle))
            else:
                #turm right
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, 0, (diffBtwnBotMostXAndRMostX-diffBtwnLMostParallelXAndBotMostX)/(diffBtwnBotMostXAndRMostX)*turnAngle) 
                time.sleep(4)
                h.WalkToPosition(InitialiseNaoRobot.motionProxy, 0, y, 0) 
                Logger.Log("walking dimensions")
                Logger.Log(str(-y))
                Logger.Log(str(-(diffBtwnBotMostXAndRMostX-diffBtwnLMostParallelXAndBotMostX)/(diffBtwnBotMostXAndRMostX)*turnAngle))