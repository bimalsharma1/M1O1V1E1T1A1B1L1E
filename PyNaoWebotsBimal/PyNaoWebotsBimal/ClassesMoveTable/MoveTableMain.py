import LookForTable
import GoToTable
import GoToOppositeSideOfTable
import MoveTable
import LiftTable
import LandTable
import PositionToCentreOfTableSide
import SmallStepSideways
import Logger
from Utils import FileIO
from Utils import InitialiseNaoRobot
from Utils import Helper as h
from Utils import ActionHelper as a
from Queue import Queue
import threading 
import thread
import time
import BehaviourMoveToTopCornerOfObject
from SimpleBehaviours import AlignToMiddleOfTable
from SimpleBehaviours import MoveToOtherSideOfObject
#Description: Main controller to perform behaviour in logical order
class MoveTableMain:
    def Main(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)

        print "look for table"
        lookForTable = LookForTable.LookForTable() 
        lookForTable.LookForTable(initNao)

        print "go to table"
        goToTable = GoToTable.GoToTable()
        goToTable.GoToTable(initNao)

        print "move table"
        moveTable = MoveTable.MoveTable()
        moveTable.MoveTableDef(initNao, 0, 2, 0)

    def LookForTable(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)

        print "look for table"
        lookForTable = LookForTable.LookForTable() 
        lookForTable.LookForTable(initNao)

    def GoToTable(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)

        print "go to table"
        goToTable = GoToTable.GoToTable()
        goToTable.GoToTable(initNao)

    def MoveTable(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)
        
        print "move table"
        moveTable = MoveTable.MoveTable()
        moveTable.MoveTableDef(initNao, 0, 1, 0)
    
    def AlignToMiddleOfTable(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)

        print "align to middle"
        alignToMiddle = AlignToMiddleOfTable.AlignToMiddleOfTable()
        alignToMiddle.AlignToMiddleOfTable(initNao)

    def AlignToOtherSide(self, port):
        Logger.Log("MOVE  NAO") 
        print "MOVE  NAO"
        initNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        initNao.wakeUpRobot(port)
        h.AddNao(initNao)

        print "align to middle"
        alignToMiddle = MoveToOtherSideOfObject.MoveToOtherSideOfObject(initNao)
        # alignToMiddle.MoveToOtherSideOfObject(initNao)

    def LiftLandTableRepeat(self, port):
        closeToWall = False
        Logger.Log("LiftLandTableRepeat") 
        print "LiftLandTableRepeat"
        InitNao = InitialiseNaoRobot.InitialiseNaoRobot(port)
        InitNao.wakeUpRobot(port)
        h.AddNao(InitNao)

        yCntrPos = 0
        #SELCT LEADER
        if InitNao.portName == "9559":
            yCntrPos = 10
            h.SendDistanceToObjectMessage(InitNao, str(yCntrPos))
        else:
            h.SendDistanceToObjectMessage(InitNao, str(yCntrPos))
        #Wait for leader data to be available
        while not h.isLeaderDataAvailable(InitNao):
            time.sleep(2)
        print "SELECTING LEADER"
        h.SelectLeader(InitNao)

        liftLandCounter = 0
        while not closeToWall:
            #document the pre AND post conditions
            alignToMiddle = AlignToMiddleOfTable.AlignToMiddleOfTable()
            alignToMiddle.AlignToMiddleOfTable(InitNao)
            a.WalkAheadUntilCloseToLift(InitNao)
            Logger.Log("Sending ready to lift message")
            h.SendReadyToLiftMessage(InitNao,"READYTOLIFT")
            print "move table"
            moveTable = MoveTable.MoveTable()
            if InitNao.isLeader != True:
                moveTable.MoveTableDef(InitNao, 0, 1, 0)
            else:
                moveTable.MoveTableDef(InitNao, 0, 1, 0)

            FileIO.EmptyFileContents("readyToLift.txt")
            liftLandCounter += 1
            if liftLandCounter > 3:
                closeToWall = True