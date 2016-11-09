import BehaviourMoveToCornerOfObject
import BehaviourAlignToLongerSideOfObject
import Logger
from Utils import InitialiseNaoRobot

class GoToTable():
    """description of class"""
    def __init__(self, InitialiseNaoRobot):
        InitialiseNaoRobot = InitialiseNaoRobot
    def GoToTable(self):
        print "Go to table"
        Logger.Log("STARTING GoToTable")
        BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(InitialiseNaoRobot)
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(InitialiseNaoRobot)   
         #document the pre AND post conditions


