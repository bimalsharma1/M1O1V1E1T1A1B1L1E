import findObjectOfInterest
import Logger

class LookForTable:
    """description of class"""
    def LookForTable(self, motionProxy, portName):
        Logger.Log("STARTING LOOKFORTABLE")
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint = findObjectOfInterest.findObjectOfInterest(motionProxy, filenameTopCamera,filenameBottomCamera, portName)


