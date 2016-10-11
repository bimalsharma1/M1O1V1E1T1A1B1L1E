# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 04:27:34 2016

@author: bimal
"""
import config
from naoqi import ALProxy

def InitialiseFirstNao():
    motionProxy  = ALProxy("ALMotion", config.ipAddress, config.ports['port1'])
    postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports['port1']) 
    #    photoCaptureProxy = ALProxy("ALPhotoCapture", config.ipAddress, config.ports['port1'])
    
    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to Stand Init
    #postureProxy.goToPosture("StandZero", 0.5)
    #####################
    ## Enable arms control by move algorithm
    #####################
    motionProxy.setMoveArmsEnabled(True, True)
    #motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.post.moveTo(0.01, 0, 0)
    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
    return motionProxy
    
def InitialiseSecondNao():
    motionProxy  = ALProxy("ALMotion", config.ipAddress, config.ports['port2'])
    postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports['port2']) 
    
    # Wake up robot
    motionProxy.wakeUp()
    
    # Send robot to Stand Init
    #postureProxy.goToPosture("StandZero", 0.5)
    #####################
    ## Enable arms control by move algorithm
    #####################
    motionProxy.setMoveArmsEnabled(True, True)
    #~ motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.post.moveTo(0.01, 0, 0)
    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
    return motionProxy

