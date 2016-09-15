# -*- coding: utf-8 -*-
"""
Created on Sun May 01 07:21:29 2016

@author: bimal
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 15:56:26 2016

@author: bimal
"""
import argparse
import almath as m # python's wrapping of almath
import time

def WalkToPositionWithHandsUp(motionProxy, X, Y, Theta):
    #####################
    ## get robot position before move
    #####################
 # initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    #initRobotPosition1 = m.Pose2D(motionProxy1.getRobotPosition(False))
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.post.moveTo(X, Y, Theta)
    #motionProxy.waitUntilMoveIsFinished()

    

def WalkToPosition(motionProxy, X, Y, Theta):
    #####################
    ## get robot position before move
    #####################
 # initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    #initRobotPosition1 = m.Pose2D(motionProxy1.getRobotPosition(False))

    motionProxy.post.moveTo(X, Y, Theta)
    #motionProxy1.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function

    #motionProxy.waitUntilMoveIsFinished()
    #motionProxy1.waitUntilMoveIsFinished()

def WalkToPositionWaitUntilWalkFinished(motionProxy, X, Y, Theta):
    #####################
    ## get robot position before move
    #####################
 # initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
    #initRobotPosition1 = m.Pose2D(motionProxy1.getRobotPosition(False))

    motionProxy.post.moveTo(X, Y, Theta)
    #motionProxy1.post.moveTo(X, Y, Theta)
    # wait is useful because with post moveTo is not blocking function

    motionProxy.waitUntilMoveIsFinished()
    #motionProxy1.waitUntilMoveIsFinished()
    
    
 
   