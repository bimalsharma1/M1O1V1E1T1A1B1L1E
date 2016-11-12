from Utils import Helper as h
import Logger
import time

class LandTable:
    """description of class"""
    def LandTable(self, motionProxy):
        Logger.Log("STARTING LandTable")
        h.LiftWithElbowAndShouldersPutObjectDown(motionProxy)
        motionProxy.waitUntilMoveIsFinished()
        time.sleep(3)
        h.WalkToPosition(motionProxy, -0.5, 0, 0)


