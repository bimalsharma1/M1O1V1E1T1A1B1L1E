from SimpleBehaviours import FindObjectOfInterest as f
import Logger
class GoToOppositeSideOfTable(object):
    """description of class"""
    def GoToOppositeSideOfTable(self, motionProxy,portName):
        Logger.Log("STARTING GoToOppositeSideOfTable")
        naoFound = f.FindIfNaoBehindObject(motionProxy,portName)
        print naoFound


