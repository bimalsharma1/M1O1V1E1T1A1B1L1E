from Utils import Helper as h
import Logger
import time

class SmallStepSideways:
    """description of class"""
    def SmallStepSideways(self, motionProxy, X, Y, Theta):
        Logger.Log("STARTING SmallStepSideways")
        time.sleep(1)
        print "move arms"
        h.WalkToPositionWithHandsUp(motionProxy, X, Y, Theta)
        motionProxy.waitUntilMoveIsFinished()
        time.sleep(5)