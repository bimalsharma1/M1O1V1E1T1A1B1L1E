import LiftTable
import SmallStepSideways
import LandTable
import Logger

class MoveTable:
    @staticmethod
    def MoveTableDef(motionProxy, X, Y, Theta):
        print "in function"
        Logger.Log("STARTING MoveTable")

        print "lifting table"
        liftTable = LiftTable.LiftTable()
        liftTable.LiftTable(motionProxy)

        print "taking small step sideways"
        smallStepSideways = SmallStepSideways.SmallStepSideways()
        smallStepSideways.SmallStepSideways(motionProxy, X, Y, Theta)

        print "Landing table"
        landTable = LandTable.LandTable()
        landTable.LandTable(motionProxy)
        Logger.Log("MoveTable COMPLETE")