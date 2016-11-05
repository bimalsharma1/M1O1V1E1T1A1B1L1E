import BehaviourMoveToCornerOfObject
import BehaviourAlignToLongerSideOfObject
import Logger

class GoToTable(object):
    """description of class"""
    def GoToTable(self, motionProxy,portName):
        print "Go to table"
        Logger.Log("STARTING GoToTable")
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(motionProxy, portName)
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(motionProxy, portName)   
         #document the pre AND post conditions


