import findNaoObjectPositions
import Logger
class GoToOppositeSideOfTable(object):
    """description of class"""
    def GoToOppositeSideOfTable(motionProxy,portName):
        Logger.Log("STARTING GoToOppositeSideOfTable")
        naoFound = findNaoObjectPositions.findIfNaoBehindObject(motionProxy,portName)
        print naoFound


