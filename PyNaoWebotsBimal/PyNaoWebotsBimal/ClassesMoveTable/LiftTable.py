import Helper
import Logger

class LiftTable:
    """description of class"""
    def LiftTable(self, motionProxy):
        Logger.Log("STARTING LiftTable")
        Helper.LiftWithElbowAndShoulders(motionProxy) #rename to utils
        motionProxy.waitUntilMoveIsFinished()


