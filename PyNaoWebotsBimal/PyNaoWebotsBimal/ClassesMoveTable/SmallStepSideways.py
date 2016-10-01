import WalkToPosition
import Logger

class SmallStepSideways(object):
    """description of class"""
    def SmallStepSideways(motionProxy, X, Y, Theta):
        Logger.Log("STARTING SmallStepSideways")
        time.sleep(1)
        print "move arms"
        WalkToPosition.WalkToPositionWithHandsUp(motionProxy, X, Y, Theta)
        time.sleep(3)


