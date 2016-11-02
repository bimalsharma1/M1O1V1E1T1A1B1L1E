import Helper
import WalkToPosition
import Logger
import time

class LandTable:
    """description of class"""
    def LandTable(self, motionProxy):
        Logger.Log("STARTING LandTable")
        Helper.LiftWithElbowAndShouldersPutObjectDown(motionProxy)
        motionProxy.waitUntilMoveIsFinished()
        time.sleep(3)
        WalkToPosition.WalkToPosition(motionProxy, -0.5, 0, 0)


