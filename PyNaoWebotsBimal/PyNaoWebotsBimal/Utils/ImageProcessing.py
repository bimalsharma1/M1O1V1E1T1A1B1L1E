# Get an image from NAO. Display it and save it using PIL.
# Python Image Library
from PIL import Image
import numpy as np
import time
import StringIO
import time
from Utils import InitialiseNaoRobot
from naoqi import ALProxy
import cv2
import vision_definitions
#class ImageProcessing(InitialiseNaoRobot.InitialiseNaoRobot):

    # def __init__(self):       
        # motionProxy = None
        # postureProxy = None
        # camProxy = camProxy = None
        # tts = None
        # topVideoClient = None
        # bottomVideoClient = None
        # motionProxy = ALProxy("ALMotion", config.ipAddress, config.ports['port1'])
        # postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports['port1']) 
        # camProxy = camProxy = ALProxy("ALVideoDevice", IP, PORT)
        # tts = ALProxy("ALTextToSpeech", config.ipAddress, config.ports['port1'])
        # topVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kTopCamera, resolution, colorSpace, 5)
        # bottomVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kBottomCamera , resolution, colorSpace, 5)

def getImage(InitialiseNaoRobot, camera, FILENAME = None): 
        camProxy = InitialiseNaoRobot.camProxy
        topVideoClient = InitialiseNaoRobot.topVideoClient
        bottomVideoClient = InitialiseNaoRobot.bottomVideoClient
        
        #naoImage = ""
        if (camera == "TOP"):
            naoImage = camProxy.getImageRemote(topVideoClient)
        else:
            naoImage = camProxy.getImageRemote(bottomVideoClient)
        # camProxy.unsubscribe(videoClient)
        time.sleep(1)
        # Get the image size and pixel array.
        print "b"
        imageWidth = naoImage[0]
        print "s"
        imageHeight = naoImage[1]
        print "d"
        array = naoImage[6]
        print "a"
        array = np.array(array)
        
        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

        if(FILENAME != None): 
            im.save(FILENAME + ".png", "PNG") # Save the image.

        #Write data to memory
        memoryFile = StringIO.StringIO()
        im.save(memoryFile, "PNG")
        memoryFile.write(im.tostring())
        memoryFile.seek(0)
        strMemoryFile = memoryFile.getvalue()
        memoryFile.close()
        # time.sleep(1)
        #r, im = cv2.imencode("png",array)
        return strMemoryFile
        #  im.show()

