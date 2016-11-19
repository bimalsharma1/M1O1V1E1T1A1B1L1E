import Logger
from Utils import InitialiseNaoRobot
from SimpleBehaviours import MoveToCornerOfObject
from SimpleBehaviours import AlignToLongerSideOfObject
from Utils import Helper as h

class GoToTable:
    """description of class"""
    def GoToTable(self, InitialiseNaoRobot):
        print "Go to table"
        Logger.Log("STARTING GoToTable")
        print "Go to corner of table: start"
        MoveToCornerOfObject.MoveToCornerOfObject(InitialiseNaoRobot)
        print "Go to Longer side of table: start"
        AlignToLongerSideOfObject.AlignToLongerSideOfObject(InitialiseNaoRobot)   
         #document the pre AND post conditions
        Logger.Log("Sending ready to lift message")
        h.SendReadyToLiftMessage(InitialiseNaoRobot,"READYTOLIFT")
        

