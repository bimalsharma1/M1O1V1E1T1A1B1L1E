import findObjectOfInterest
import Logger
from Utils import InitialiseNaoRobot

class LookForTable:
    """description of class"""
    def __init__(self, InitialiseNaoRobot):
        InitialiseNaoRobot = InitialiseNaoRobot
    def LookForTable(self): 
        #inherit common vars
        Logger.Log("STARTING LOOKFORTABLE")
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint = findObjectOfInterest.findObjectOfInterest(InitialiseNaoRobot, filenameTopCamera,filenameBottomCamera)

