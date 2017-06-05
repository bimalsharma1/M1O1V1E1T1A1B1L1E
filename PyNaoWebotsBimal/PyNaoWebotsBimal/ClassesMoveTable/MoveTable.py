import LiftTable
import SmallStepSideways
import LandTable
import Logger
import time
from Utils import InitialiseNaoRobot
from Utils import Helper as h

#Description: Perform behaviour MoveTable
class MoveTable:
    def MoveTableDef(self, InitialiseNaoRobot, X, Y, Theta):
        print "in function"
        Logger.Log("STARTING MoveTable")

        while h.GetReadyToLift(InitialiseNaoRobot) == False:
            time.sleep(1)

        print "lifting table"
        liftTable = LiftTable.LiftTable()
        liftTable.LiftTable(InitialiseNaoRobot.motionProxy)

        print "taking small step sideways"
        smallStepSideways = SmallStepSideways.SmallStepSideways()
        if(InitialiseNaoRobot.isLeader == True):#to make both robots walk on the same side
            smallStepSideways.SmallStepSideways(InitialiseNaoRobot.motionProxy, X, -Y, Theta)
            print "moving Y value NEGATIVE"
            print str(-Y)
            Logger.Log("moving Y value NEGATIVE")
            Logger.Log(str(-Y))
        else:
            smallStepSideways.SmallStepSideways(InitialiseNaoRobot.motionProxy, X, Y, Theta)
            print "moving Y value POSITIVE"
            print str(Y)
            Logger.Log("moving Y value POSITIVE")
            Logger.Log(str(Y))

        print "Landing table"
        landTable = LandTable.LandTable()
        landTable.LandTable(InitialiseNaoRobot.motionProxy)
        Logger.Log("MoveTable COMPLETE")