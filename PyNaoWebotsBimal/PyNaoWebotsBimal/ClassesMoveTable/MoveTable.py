import LiftTable
import SmallStepSideways
import LandTable
import Logger
import time
from Utils import InitialiseNaoRobot
from Utils import Helper as h

class MoveTable:
    def MoveTableDef(self, InitialiseNaoRobot, X, Y, Theta):
        print "in function"
        Logger.Log("STARTING MoveTable")

        while h.GetReadyToLift(InitialiseNaoRobot) == False:
            time.sleep(1)

        print "lifting table"
        liftTable = LiftTable.LiftTable()
        liftTable.LiftTable(InitialiseNaoRobot.motionProxy)

        if(InitialiseNaoRobot.isLeader):#to make both robots walk on the same side
            Y = -1 * Y
        print "taking small step sideways"
        smallStepSideways = SmallStepSideways.SmallStepSideways()
        smallStepSideways.SmallStepSideways(InitialiseNaoRobot.motionProxy, X, Y, Theta)

        print "Landing table"
        landTable = LandTable.LandTable()
        landTable.LandTable(InitialiseNaoRobot.motionProxy)
        Logger.Log("MoveTable COMPLETE")