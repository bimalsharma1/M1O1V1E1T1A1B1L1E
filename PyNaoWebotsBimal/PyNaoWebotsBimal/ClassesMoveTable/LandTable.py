import Helper
import WalkToPosition
class LandTable(object):
    """description of class"""
    def LandTable(motionProxy):
        Logger.Log("STARTING LandTable")
        Helper.LiftWithElbowAndShouldersPutObjectDown(motionProxy)
        time.sleep(3)
        WalkToPosition.WalkToPosition(motionProxy, -0.1, 0, 0)


