# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 15:56:26 2016

@author: bimal
"""
import argparse
import almath as m # python's wrapping of almath
import time
import Logger
import findNaoObjectPositions
from Utils import Helper as h

def LiftTable(motionProxy, portName):
    time.sleep(2)
    readyToLift = findNaoObjectPositions.findIfOtherNaoReadyToMoveTable(motionProxy, portName)
    print "ready STATUS"
    print readyToLift

    Y = 1
    h.WalkToPosition(motionProxy,0, Y, 0)


def BehaviourMoveTable(motionProxy,  X, Y, Theta):

#    motionProxy.setStiffnesses("Head", 0.5)
    # go to an init head pose.
    #names  = ["HeadYaw", "HeadPitch","RShoulderPitch","LShoulderPitch","LShoulderRoll","RElbowRoll"]
    #angles = [0., 0.,0.,0.,0.,0.]
    #times  = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    #isAbsolute = True
    #motionProxy.angleInterpolation(names, angles, times, isAbsolute)
    #then up to lift
    time.sleep(2)
    names  = "RShoulderPitch"
    angles = 0
    fractionMaxSpeed  = .1
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    #motionProxy1.setAngles(names, angles, fractionMaxSpeed)
    
    names  = "LShoulderPitch"
    angles = 0
    fractionMaxSpeed  = .1
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    #motionProxy1.setAngles(names, angles, fractionMaxSpeed)
    
    motionProxy.waitUntilMoveIsFinished()
    #motionProxy1.waitUntilMoveIsFinished()    
    
    time.sleep(3)
    #then on  robot to the side
    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.post.moveTo(0, Y, 0)
    motionProxy.waitUntilMoveIsFinished()

        
    time.sleep(2)
    ####put hands down
    names  = "RShoulderPitch"
    angles = 2.08
    fractionMaxSpeed  = .01
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    
    names  = "LShoulderPitch"
    angles = 2.08
    fractionMaxSpeed  = .01
    motionProxy.setAngles(names, angles, fractionMaxSpeed)
    
    motionProxy.waitUntilMoveIsFinished()
    #####################
    ## get robot position after move
    #####################
    endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition

    # return an angle between ]-PI, PI]
    robotMove.theta = m.modulo2PI(robotMove.theta)
    print "Robot Move:", robotMove, robotMove1

    # Go to rest position
#    motionProxy.rest()