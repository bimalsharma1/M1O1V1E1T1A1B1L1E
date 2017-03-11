# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 21:28:02 2016

@author: bimal
"""

ports = dict(
    port1 = 9557,
    port2 = 9559,
    )
ipAddress = '127.0.0.1'

#variables set for camera
resolution = 2    # VGA
colorSpace = 11   # RGB

imageWidth = 640
imageHeight = 480

maxTurnAngleForVCentre = 25
acceptableErrorForVCentre = 30

InitialLongerSideOfTable = ""
Leader = ""   # config is updated witht he leader name

WirelessMessages = [] #storage for simulated wireless