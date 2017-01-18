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
from PIL import Image
import numpy as np
import StringIO
from Utils import InitialiseNaoRobot

#GET rect longer side
fileName = "TablePicToSelectLongerSide9559.png"
# imT = cv2.imread(fileName)   #png
initNao = InitialiseNaoRobot.InitialiseNaoRobot('port1')
# initNao.wakeUpRobot('9559')
imT = ip.getImage(initNao, "TOP", fileName)
print "start detect"
xCntrPos, yCntrPos, ObjFoundBtmCam, closestPnt,contourList,bl,br,tl,tr = d.DetectColour(fileName, "", imT)
# fourCorners = [contourList[0], contourList[1], contourList[2], contourList[3]]

# warped = p.getPerspectiveTransformFromFile(imT, fileName)
# print "a"
# xCntrPos, yCntrPos, maxBtmCamAreaCovrd, closestPnt,contourList,bl,br,tl,tr = d.DetectColour("warped.png", "", warped)    