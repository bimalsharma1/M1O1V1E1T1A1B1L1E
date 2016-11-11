import BehaviourMoveToCornerOfObject
import BehaviourAlignToLongerSideOfObject
import Logger
from Utils import InitialiseNaoRobot

class GoToTable:
    """description of class"""
    def GoToTable(self, InitialiseNaoRobot):
        print "Go to table"
        Logger.Log("STARTING GoToTable")
        print "Go to corner of table: start"
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(InitialiseNaoRobot)
        print "Go to Longer side of table: start"
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(InitialiseNaoRobot)   
         #document the pre AND post conditions


