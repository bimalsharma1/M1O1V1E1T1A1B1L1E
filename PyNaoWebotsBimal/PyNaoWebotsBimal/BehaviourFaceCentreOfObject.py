import almath # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
import ALPhotoCapture
import config
import vision_getandsaveimage
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
from Utils import Helper as h
import sys
import findObjectOfInterest
import os
import DetectCornersFast
import Logger

def behaviourFaceCentreOfObject(motionProxy, portName):  
        #InitialiseHeadAndShoulders.InitialiseHeadAndShoulders(motionProxy,motionProxy1)
        lastKnownPositionOfObject = ""
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        fourtyFiveDegreeInRadians = 0.8
        turnAngle = 0.00
        count = 0
        names = "HeadYaw"
        times      = [1.0]
        isAbsolute = True
        percentOfImageCoveredWithContour=0

        X=0
        Y = -0.0 # move left or right
        #positive theta is anticlockwise
        Theta = 1 # amount to turn around in radians
        #get whole object in top picture
        #trying to get whole object in picture
        print "TRYING TO GET WHOLE OBJECT IN PICTURE"
        wholeObjectInTopPicture = False
        while not (wholeObjectInTopPicture):   
            bottomMostPoint=[0,0]       
            #use top camera only if bottom camera cannot see ...
            imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
            xCentrePostion, yCentrePosition, objectFoundOnBottomCamera, bottomMostPoint,contourList,bl,br,tl,tr = DetectRedBlueYellowGrey.detectColouredObject(filenameTopCamera + ".png", "", imT)   
            print "bottommost point"
            print bottomMostPoint[0]
            turnAngle = 0.2
            
            print "CENTRE POSITION IS ", xCentrePostion
        
            if (br[0]>639 or tr[0]>639):
                if (bl[0]>1 and tl[0]>1):
                    h.WalkToPosition(motionProxy, 0, 0, -turnAngle)
                    wholeObjectInTopPicture = False

            if (bl[0]<1 or tl[0]<1):
                if (br[0]<639 and tr[0]<639):
                    h.WalkToPosition(motionProxy, 0, 0, turnAngle)
                    wholeObjectInTopPicture = False
               
            if (br[0]<640 and tr[0]<640 and bl[0]>0 and tl[0]>0):
                wholeObjectInTopPicture = True