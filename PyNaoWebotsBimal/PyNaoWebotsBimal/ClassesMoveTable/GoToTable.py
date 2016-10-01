import BehaviourMoveToCornerOfObject
import Logger

class GoToTable(object):
    """description of class"""
    def GoToTable(motionProxy,portName):
        Logger.Log("STARTING GoToTable")
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(motionProxy, portName)
         


