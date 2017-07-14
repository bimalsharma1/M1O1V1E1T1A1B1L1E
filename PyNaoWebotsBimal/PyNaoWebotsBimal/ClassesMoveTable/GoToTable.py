import Logger
from Utils import InitialiseNaoRobot
from SimpleBehaviours import MoveToCornerOfObject
from SimpleBehaviours import AlignToLongerSideOfObject
from SimpleBehaviours import AlignToMiddleOfTable
from Utils import Helper as h

class GoToTable:
    """Perform Behaviour GoToTable"""
    def GoToTable(self, InitialiseNaoRobot):
        print "Go to table"
        Logger.Log("STARTING GoToTable")
        print "Go to corner of table: start"
        IgnoreAlignToLongerSide = MoveToCornerOfObject.MoveToCornerOfObject(InitialiseNaoRobot)
        if not IgnoreAlignToLongerSide:
            print "Go to Longer side of table: start"
            AlignToLongerSideOfObject.AlignToLongerSideOfObject(InitialiseNaoRobot)   
         #document the pre AND post conditions
        alignToMiddle = AlignToMiddleOfTable.AlignToMiddleOfTable()
        alignToMiddle.AlignToMiddleOfTable(InitialiseNaoRobot)

        Logger.Log("Sending ready to lift message")
        h.SendReadyToLiftMessage(InitialiseNaoRobot,"READYTOLIFT")