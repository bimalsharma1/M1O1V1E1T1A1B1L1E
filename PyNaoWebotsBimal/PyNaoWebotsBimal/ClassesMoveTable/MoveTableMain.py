import LookForTable
import GoToTable
import GoToOppositeSideOfTable
import MoveTable
import LiftTable
import LandTable
import PositionToCentreOfTableSide
import SmallStepSideways
import Logger
from Utils import InitialiseNaoRobot
from Utils import Helper as h
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
        moveTable.MoveTableDef(initNao, 0, 1, 0)

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