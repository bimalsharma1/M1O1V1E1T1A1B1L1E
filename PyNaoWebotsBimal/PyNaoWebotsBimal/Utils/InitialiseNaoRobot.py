# Get an image from NAO. Display it and save it using PIL.
# Python Image Library
from PIL import Image
import numpy as np
from naoqi import ALProxy
import cv2
import vision_definitions
import time
import StringIO
import Helper
import Logger
import config
import comms9557

class InitialiseNaoRobot:
    
    motionProxy = None
    postureProxy = None
    camProxy = camProxy = None
    tts = None
    topVideoClient = None
    bottomVideoClient = None
    portName = None

    @staticmethod
    def __init__(self, port):
        motionProxy = ALProxy("ALMotion", config.ipAddress, config.ports[port])
        postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports[port]) 
        camProxy = camProxy = ALProxy("ALVideoDevice", config.ipAddress, config.ports[port])
        tts = ALProxy("ALTextToSpeech", config.ipAddress, config.ports[port])
        topVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kTopCamera, config.resolution, config.colorSpace, 5)
        bottomVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kBottomCamera , config.resolution, config.colorSpace, 5)
        portName = port
        
        motionProxy.wakeUp()
        motionProxy.moveInit()
        motionProxy.setStiffnesses("Body", 1.0)
        motionProxy.setMoveArmsEnabled(True, True)
        motionProxy.post.moveTo(0.01, 0, 0)
        motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        Helper.AddNao(config.ipAddress, config.ports[port])
        print config.ipAddress, config.ports[port]
        print "woken up"
        time.sleep(3)

    def getMotionProxy(self):
        return self.motionProxy

    def getCamProxy(self):
        return self.camProxy

    def getTopVideoClient (self):
        return self.topVideoClient 

    def getBottomVideoClient(self):
        return self.bottomVideoClient

    # def get():
    #     return (motionProxy, postureProxy, camProxy, topVideoClient, bottomVideoClient)
    
#    # @staticmethod
#     def InitialiseNao(IP, PORT):
#         # motionProxy  = ALProxy("ALMotion", IP, PORT)
#         # postureProxy = ALProxy("ALRobotPosture", IP, PORT) 
#         # tts = ALProxy("ALTextToSpeech", IP, PORT)
#         # tts.say("Hello, world, I have woken up, I have woken up, I have woken up, I have woken up")

#         # Wake up robot
#         motionProxy.wakeUp()
#         motionProxy.moveInit()
#         motionProxy.setStiffnesses("Body", 1.0)
        
#         # Send robot to Stand Init
#         #postureProxy.goToPosture("StandZero", 0.5)
#         #####################
#         ## Enable arms control by move algorithm
#         #####################
#         motionProxy.setMoveArmsEnabled(True, True)
#         #motionProxy.setMoveArmsEnabled(False, False)
#         motionProxy.post.moveTo(0.01, 0, 0)
#         #####################
#         ## FOOT CONTACT PROTECTION
#         #####################
#         #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
#         motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

#         ### INITIALISE TOP AND BOTTOM CAMERA
#         time.sleep(1)
#         #separate proxy from actual call
#         # camProxy = ALProxy("ALVideoDevice", IP, PORT)
#         # resolution = 2    # VGA
#         # colorSpace = 11   # RGB

#         # topVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kTopCamera, resolution, colorSpace, 5)
#         # bottomVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kBottomCamera , resolution, colorSpace, 5)
#         # time.sleep(1)

#         #add own ip address to list
#         Helper.AddNao(IP, PORT)
#         print PORT
#         print "woken up"

#         return motionProxy
    
    def getImage(self, camProxy, videoClient, FILENAME = None):
        naoImage = camProxy.getImageRemote(videoClient)
        camProxy.unsubscribe(videoClient)
        time.sleep(1)
        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]
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

