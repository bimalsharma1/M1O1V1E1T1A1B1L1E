import BehaviourMoveToCornerOfObject
import Logger

class GoToTable(object):
    """description of class"""
    def GoToTable(self, motionProxy,portName):
        Logger.Log("STARTING GoToTable")
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(motionProxy, portName)
         


