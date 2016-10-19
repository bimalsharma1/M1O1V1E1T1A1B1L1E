# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 04:27:34 2016

@author: bimal
"""
import config
from naoqi import ALProxy
import comms9557
import comms9559
import Helper

def InitialiseFirstNao():
    motionProxy  = ALProxy("ALMotion", config.ipAddress, config.ports['port1'])
    postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports['port1']) 
    tts = ALProxy("ALTextToSpeech", config.ipAddress, config.ports['port1'])
    tts.say("Hello, world, I have woken up, I have woken up, I have woken up, I have woken up")

    #    photoCaptureProxy = ALProxy("ALPhotoCapture", config.ipAddress, config.ports['port1'])
    
    # Wake up robot
    motionProxy.wakeUp()
    motionProxy.moveInit()
    motionProxy.setStiffnesses("Body", 1.0)
    
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

    #add own ip address to list
    Helper.AddNao(config.ipAddress, config.ports['port1'])
    print config.ports['port1']
    print "woken up"

    return motionProxy
    
def InitialiseSecondNao():
    motionProxy  = ALProxy("ALMotion", config.ipAddress, config.ports['port2'])
    postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports['port2']) 
    tts = ALProxy("ALTextToSpeech", config.ipAddress, config.ports['port2'])
    tts.say("Hello, world, I have woken up, I have woken up, I have woken up, I have woken up")

    
    # Wake up robot
    motionProxy.wakeUp()
    motionProxy.moveInit()
    motionProxy.setStiffnesses("Body", 1.0)
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

    #add own ip address to list
    Helper.AddNao(config.ipAddress, config.ports['port2'])
    print config.ports['port2']
    print "woken up"
    return motionProxy

