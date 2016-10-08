import BehaviourAlignToLongerSideOfObject
import Logger

class PositionToCentreOfTableSide(object):
    """description of class"""
    def PositionToCentreOfTableSide(self, motionProxy, portName):
        Logger.Log("STARTING PositionToCentreOfTableSide")
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(motionProxy, portName)  


