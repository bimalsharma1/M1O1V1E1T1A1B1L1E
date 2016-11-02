# -*- coding: utf-8 -*-
"""
Created on Sun May 01 07:26:37 2016

@author: bimal
"""

import argparse
import almath as m # python's wrapping of almath
import time


def InitialiseHeadAndShoulders(motionProxy, motionProxy1):

#    motionProxy.setStiffnesses("Head", 0.5)
    # go to an init head pose.
    names  = ["HeadYaw", "HeadPitch","RShoulderPitch","LShoulderPitch","LShoulderRoll","RElbowRoll"]
    angles = [0., 0.,0.,0.,0.,0.]
    times  = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angles, times, isAbsolute)
    motionProxy1.angleInterpolation(names, angles, times, isAbsolute)


    ####put hands down
    names  = "RShoulderPitch"
    angles = 2.08
    fractionMaxSpeed  = .3
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    motionProxy1.setAngles(names, angles, fractionMaxSpeed)
    
    names  = "LShoulderPitch"
    angles = 2.08
    fractionMaxSpeed  = .3
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    motionProxy1.setAngles(names, angles, fractionMaxSpeed)
    
    motionProxy.waitUntilMoveIsFinished()
    motionProxy1.waitUntilMoveIsFinished()
   