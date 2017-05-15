from SimpleBehaviours import AlignToLongerSideOfObject as a
import Logger

class PositionToCentreOfTableSide(object):
    #Description: PositionToCentreOfTableSide
    def PositionToCentreOfTableSide(self, motionProxy, portName):
        Logger.Log("STARTING PositionToCentreOfTableSide")
        a.AlignToLongerSideOfObject(motionProxy, portName)  


