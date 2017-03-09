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

class MoveTableMain:
    """description of class"""
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