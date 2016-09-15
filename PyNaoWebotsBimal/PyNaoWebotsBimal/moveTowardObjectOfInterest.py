# -*- encoding: UTF-8 -*-

'''Main progrm written by Bimal Sharma to start Nao control'''

import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import sys
import os
import BehaviourFindObject
import BehaviourMoveToCornerOfObject
import BehaviourFaceCentreOfObject
import BehaviourAlignToLongerSideOfObject
import BehaviourWalkToLiftRangeOfObject
import BehaviourMoveTable
import cv2
import numpy as np
import Logger
from datetime import datetime
import config
import Helper
import DetectRedBlueYellowGrey
import vision_getandsaveimage
import findNaoObjectPositions
import BehaviourCommunicateReadyToLiftStatus
import BehaviourMoveTable

def moveTowardObjectOfInterest(motionProxy, portName):
    try: 
        Logger.Log("STARTING SIMULATION")
        BehaviourFindObject.behaviourFindObject(motionProxy, portName)
        naoFound = findNaoObjectPositions.findIfNaoBehindObject(motionProxy,portName)
        print naoFound
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(motionProxy, portName)
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(motionProxy, portName)    
    except Exception as e:
        print e


