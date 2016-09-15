# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 16:05:04 2016

@author: bimal
"""
# -*- encoding: UTF-8 -*-

# This is just an example script that shows how images can be accessed
# through ALVideoDevice in python.
# Nothing interesting is done with the images in this example.

from naoqi import ALProxy
import vision_definitions


def PhotoCapture(IP, PORT):
    ####
    # Create proxy on ALVideoDevice
    
    print "Creating ALVideoDevice proxy to ", IP  
    camProxy = ALProxy("ALVideoDevice", IP, PORT) 
    ####
    # Register a Generic Video Module
    
    resolution = vision_definitions.kQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 30
    nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)
    print nameId
    
#strMyClientName = self.getName();
#self.strMyClientName = self.avd.subscribeCamera( strMyClientName, 0, 1, 13, 5 );
#This is more specifically what I used. 0 is the top camera, 1 is the resolution (kQVGA), 13 gave me an RGB colospace, and 5 is just the framerate.    
         
    print 'getting images in local'
    for i in range(0, 20):
      camProxy.getImageLocal(nameId)
      camProxy.releaseImage(nameId)
      
    resolution = vision_definitions.kQQVGA
    camProxy.setResolution(nameId, resolution)
    
    print 'getting images in remote'
    for i in range(0, 20):
      camProxy.getImageRemote(nameId)
    
    camProxy.unsubscribe(nameId)
    
    print 'end of gvm_getImageLocal python script'