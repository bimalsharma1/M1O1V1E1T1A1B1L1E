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
from Queue import Queue
import threading 
import thread
import time
import BehaviourMoveToTopCornerOfObject

class MoveTableMain(object):
    """description of class"""
    def Main(self):
        Logger.Log("MOVE FIRST NAO") 
        print "MOVE FIRST NAO"

        initNao1 = InitialiseNaoRobot.InitialiseNaoRobot('port1')
        initNao1.wakeUpRobot('port1')

        # initNao2 = InitialiseNaoRobot.InitialiseNaoRobot("port2")

        print "look for table"
        lookForTable1 = LookForTable.LookForTable() 
        lookForTable1.LookForTable(initNao1)
        # lookForTable2 = LookForTable.LookForTable(initNao2) 

        print "go to table"
        goToTable1 = GoToTable.GoToTable()
        goToTable1.GoToTable(initNao1)
        # goToTable2 = GoToTable.GoToTable(initNao2)

        print "move table"
        moveTable1 = MoveTable.MoveTable()
        moveTable1.MoveTableDef(initNao1, 0, 1, 0)
        # moveTable2 = MoveTable.MoveTable(initNao2, 0, -1, 0)
        # moveTable1.MoveTableDef(self,initNao1, 0, 1, 0)
        # moveTable2.MoveTableDef(self,initNao2, 0, -1, 0)
        #goToTable.GoToTable(motionProxy, portName1)
        # print "before go to tabkle threaD"
        # t = threading.Thread(target=goToTable1.GoToTable, args=(motionProxy1, portName1))    
        # t.start()
        # #t.join()#for concurrency
        # #Helper.LiftWithElbowAndShoulders(motionProxy)
        # t2 = threading.Thread(target=goToTable2.GoToTable, args=(motionProxy2, portName2))
        # t2.start()
        # t2.join()#for concurrency
        # t.join()

        #goToTable = GoToTable.GoToTable()
        #goToTable.GoToTable(motionProxy, portName1)

        # print "calling MoveTable class"
        # moveTable1 = MoveTable.MoveTable()
        # moveTable2 = MoveTable.MoveTable()
        # print "call func"
        # t3 = threading.Thread(target=moveTable1.MoveTableDef, args=(motionProxy1, 0, 1, 0))
        # t3.start()
        # t4 = threading.Thread(target=moveTable2.MoveTableDef, args=(motionProxy2, 0, -1, 0))
        # t4.start()
        
        #moveTable1.MoveTableDef(motionProxy1, 0, 4, 0)  
        #moveTable2.MoveTableDef(motionProxy2, 0, -4, 0)


        #    moveTableWithTwoRobots.Main(motionProxy, 0, 2, 0)
        #LookForTable.LookForTable(motionProxy)
        #GoToTable.GoToTable(motionProxy)
        #MoveTable.MoveTable(motionProxy, X, Y, Theta)



