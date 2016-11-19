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
from Utils import DetectColourInImage as d
import vision_getandsaveimage

def findIfNaoBehindObject(motionProxy, portName):
    try: 
        filenameTopCamera = "naoImageTopCamera"

        imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
        cx, cy, objectFound, bottomMostPoint, contourList,bl,br,tl,tr = d.DetectColour( "cropTop.png", "", imT,"RED")
        print cx, cy, objectFound, bottomMostPoint, contourList,bl,br,tl,tr

        image = cv2.imdecode(np.fromstring(imT, dtype='uint8'), cv2.IMREAD_UNCHANGED)
        cv2.imwrite("croptop.png", image)
        print image
    
        tlx=tl[0]
        trx = tr[0]
        tly=tl[1]
       
        print "HEIGHT IS ", str(contourList[4][0])
        yDiff = 480 # int(contourList[4,0]) # to get the height of pic
        print tlx, tly, trx
        print yDiff
        cropped = image[tly:yDiff,tlx:trx] #[y1:y2, x1:x2]
        cv2.imwrite("cropped.png", cropped)

        print "cropping done"
        #find blue in picture
        colourFound = d.DetectColourWithoutDetails(cropped,"BLUE")
        print colourFound
        return colourFound
      
    except Exception as e:
        print e
        return False


def findIfOtherNaoReadyToMoveTable(motionProxy, portName):
    try: 
        filenameTopCamera = "naoImageTopCamera"

        imT = vision_getandsaveimage.showNaoImageTopCam(config.ipAddress, config.ports[portName], filenameTopCamera)
        cx, cy, objectFound, bottomMostPoint, contourList,bl,br,tl,tr = d.DetectColour( "cropReadyToMove.png", "", imT,"RED")
        print cx, cy, objectFound, bottomMostPoint, contourList,bl,br,tl,tr

        image = cv2.imdecode(np.fromstring(imT, dtype='uint8'), cv2.IMREAD_UNCHANGED)
        cv2.imwrite("croptopReadyToMove.png", image)
        print image

        tlx=tl[0]-10 #add some extra pixels to incerease accuracy , any left over colour close to object is removed
        trx = tr[0]+10
        tly=tl[1]
        bly=bl[1]
        

        #set the rectangle to white
        #croppedReadyToMove = np.zeros(image.shape,np.uint8)
        #croppedReadyToMove[y:y+h,x:x+w] = image[y:y+h,x:x+w]
        croppedReadyToMove = image
        croppedReadyToMove[0:480, tlx:trx] = 255 #img[trx:340, tlx:trx]
        cv2.imwrite("croppedReady.png", croppedReadyToMove)

        #noe crop image
        croppedReadyToMove = croppedReadyToMove[tly:bly,0:640] #[y1:y2, x1:x2]
        cv2.imwrite("croppedReady1.png", croppedReadyToMove)
       
        print "cropping done"
        #find blue in picture
        colourFound = d.DetectColourWithoutDetails(croppedReadyToMove,"RED")
        print colourFound
        return colourFound
      
    except Exception as e:
        print e
        return False


