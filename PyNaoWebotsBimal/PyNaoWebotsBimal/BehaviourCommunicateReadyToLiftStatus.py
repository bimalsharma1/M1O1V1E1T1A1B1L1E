import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import cv2
import numpy as np
import Logger
from datetime import datetime
import config
import Helper
import vision_getandsaveimage

def CommunicateReadyToLift(motionProxy):
    time.sleep(5)
    Helper.CommunicateReadyToLift(motionProxy)

