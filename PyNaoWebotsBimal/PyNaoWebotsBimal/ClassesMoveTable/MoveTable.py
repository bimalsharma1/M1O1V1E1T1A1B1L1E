import LiftTable
import SmallStepSideways
import LandTable
import Logger

class MoveTable(object):
    """description of class"""
    def MoveTable(motionProxy, X, Y, Theta):
        Logger.Log("STARTING MoveTable")
        LiftTable.LiftTable(motionProxy)
        SmallStepSideways.SmallStepSideways(motionProxy, X, Y, Theta)
        LandTable.LandTable(motionProxy)
        Logger.Log("MoveTable COMPLETE")


