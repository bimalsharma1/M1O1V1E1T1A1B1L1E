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
from SimpleBehaviours import MoveToCornerOfObject as m
import BehaviourFaceCentreOfObject
from SimpleBehaviours import AlignToLongerSideOfObject as a
import BehaviourWalkToLiftRangeOfObject
import BehaviourMoveTable
import cv2
import numpy as np
import Logger
from datetime import datetime
import config
import Helper
from Utils import DetectColourInImage
import vision_getandsaveimage
from SimpleBehaviours import FindObjectOfInterest as f
import BehaviourCommunicateReadyToLiftStatus
import BehaviourMoveTable

def moveTowardObjectOfInterest(motionProxy, portName):
    try: 
        Logger.Log("STARTING SIMULATION")
        BehaviourFindObject.behaviourFindObject(motionProxy, portName)
        naoFound = f.FindIfNaoBehindObject(motionProxy,portName)
        print naoFound
        m.MoveToCornerOfObject(motionProxy, portName)
        m.AlignToLongerSideOfObject(motionProxy, portName)    
    except Exception as e:
        print e


