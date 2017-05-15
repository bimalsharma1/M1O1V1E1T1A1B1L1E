from SimpleBehaviours import FindObjectOfInterest as f
from SimpleBehaviours import MoveToOtherSideOfObject as m
import Logger
class GoToOppositeSideOfTable(object):
    """# Description: Perform behaviour GoToOppositeSideOfTable"""
    def GoToOppositeSideOfTable(self, motionProxy,portName):
        Logger.Log("STARTING GoToOppositeSideOfTable")
        naoFound = f.FindIfNaoBehindObject(motionProxy,portName)
        
        print naoFound


