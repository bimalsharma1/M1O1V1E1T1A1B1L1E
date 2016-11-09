import LiftTable
import SmallStepSideways
import LandTable
import Logger
from Utils import InitialiseNaoRobot

class MoveTable:
    def __init__(self, InitialiseNaoRobot, X, Y, Theta):
        InitialiseNaoRobot = InitialiseNaoRobot
    def MoveTableDef(self):
        print "in function"
        Logger.Log("STARTING MoveTable")

        print "lifting table"
        liftTable = LiftTable.LiftTable()
        liftTable.LiftTable(InitialiseNaoRobot.motionProxy)

        print "taking small step sideways"
        smallStepSideways = SmallStepSideways.SmallStepSideways()
        smallStepSideways.SmallStepSideways(InitialiseNaoRobot.motionProxy, X, Y, Theta)

        print "Landing table"
        landTable = LandTable.LandTable()
        landTable.LandTable(InitialiseNaoRobot.motionProxy)
        Logger.Log("MoveTable COMPLETE")