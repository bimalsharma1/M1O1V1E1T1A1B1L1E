import findObjectOfInterest
import Logger
from Utils import InitialiseNaoRobot

class LookForTable:
    """description of class"""
    def LookForTable(self, InitialiseNaoRobot): 
        #inherit common vars
        Logger.Log("STARTING LOOKFORTABLE")
        print "STARTING LOOKFORTABLE"
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint = findObjectOfInterest.findObjectOfInterest(InitialiseNaoRobot, filenameTopCamera,filenameBottomCamera)
        print "ENDING LOOKFORTABLE"
