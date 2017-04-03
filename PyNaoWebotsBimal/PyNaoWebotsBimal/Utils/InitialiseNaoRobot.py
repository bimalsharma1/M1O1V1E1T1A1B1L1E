# Get an image from NAO. Display it and save it using PIL.
# Python Image Library
from naoqi import ALProxy
import vision_definitions
import time
import Logger
import config
from Utils import Helper as h
import FileIO

class InitialiseNaoRobot:
    motionProxy = None
    postureProxy = None
    camProxy = camProxy = None
    tts = None
    topVideoClient = None
    bottomVideoClient = None
    portName = None
    ipAddress = None
    isLeader = False
    ListOfNaosDetected = []
    ReadyToLiftMessages = []
    MessagesSent = []
    MessagesReceived = []
    #collection of all Nao robots detected, can make multi dim by adding ListOfNaosDetected.append([id,leader])
    #keep 4 dim list ListOfNaosDetected.append([ipAddress+Port, [MsgReceived], [MsgSent]])
    #to find index myList.index("revolves")

    @staticmethod
    def __init__(port):
        # print "start initialise"
        InitialiseNaoRobot.motionProxy = ALProxy("ALMotion", config.ipAddress, config.ports[port])
        InitialiseNaoRobot.postureProxy = ALProxy("ALRobotPosture", config.ipAddress, config.ports[port]) 
        InitialiseNaoRobot.camProxy = camProxy = ALProxy("ALVideoDevice", config.ipAddress, config.ports[port])
        InitialiseNaoRobot.tts = ALProxy("ALTextToSpeech", config.ipAddress, config.ports[port])
        InitialiseNaoRobot.topVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kTopCamera, config.resolution, config.colorSpace, 5)
        InitialiseNaoRobot.bottomVideoClient = camProxy.subscribeCamera("python_client",vision_definitions.kBottomCamera , config.resolution, config.colorSpace, 5)
        InitialiseNaoRobot.portName = config.ports[port]
        InitialiseNaoRobot.ipAddress = config.ipAddress
        config.loggingId = str(config.ipAddress) + "-" + str(config.ports[port])
        isLeader = False
        ListOfNaosDetected = []
        ReadyToLiftMessages = []
        MessagesSent = []
        MessagesReceived = []

    # @staticmethod 
    def wakeUpRobot(self, port):
        print "wake up robot"
        self.motionProxy.wakeUp()
        self.motionProxy.moveInit()
        self.motionProxy.setStiffnesses("Body", 1.0)
        self.motionProxy.setMoveArmsEnabled(True, True)
        self.motionProxy.post.moveTo(0.01, 0, 0)
        self.motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        print config.ipAddress, config.ports[port]
        print "woken up"
        FileIO.EmptyFileContents("readyToLift.txt")
        time.sleep(3)

    def getMotionProxy(self):
        return self.motionProxy

    def getCamProxy(self):
        return self.camProxy

    def getTopVideoClient (self):
        return self.topVideoClient 

    def getBottomVideoClient(self):
        return self.bottomVideoClient

    