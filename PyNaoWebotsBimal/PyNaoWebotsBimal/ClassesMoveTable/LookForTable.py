import findObjectOfInterest

class LookForTable(object):
    """description of class"""
    def LookForTable(motionProxy, portName):
        Logger.Log("STARTING LOOKFORTABLE")
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        xCentrePostion, yCentrePosition, headLookingPosition, ObjectFound, bottomMostPoint = findObjectOfInterest.findObjectOfInterest(motionProxy, filenameTopCamera,filenameBottomCamera, portName)


