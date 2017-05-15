import Logger
from Utils import InitialiseNaoRobot
from SimpleBehaviours import FindObjectOfInterest as f

class LookForTable:
    """Perform Behaviour LookForTable"""
    def LookForTable(self, InitialiseNaoRobot): 
        #inherit common vars
        Logger.Log("STARTING LOOKFORTABLE")
        print "STARTING LOOKFORTABLE"
        filenameTopCamera = "naoImageTopCamera"
        filenameBottomCamera = "naoImageBottomCamera"
        xCntrPos, yCntrePos, headPos, objFound, btmPnt = f.FindObjectOfInterest(InitialiseNaoRobot, filenameTopCamera,filenameBottomCamera)
        print "ENDING LOOKFORTABLE"
