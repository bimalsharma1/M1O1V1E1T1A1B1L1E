import LookForTable
import GoToTable
import GoToOppositeSideOfTable
import MoveTable
import LiftTable
import LandTable
import PositionToCentreOfTableSide
import SmallStepSideways
import Logger
import InitialiseNao
from Queue import Queue
import threading 
import thread
import time

class MoveTableMain:
    """description of class"""
    def Main(self):
        Logger.Log("MOVE FIRST NAO") 
        portName1 = 'port1'
        motionProxy1 = InitialiseNao.InitialiseFirstNao()

        Logger.Log("MOVE SECOND NAO")    
        portName2 = 'port2'
        motionProxy2 = InitialiseNao.InitialiseSecondNao()

        q = Queue()

        lookForTable = LookForTable.LookForTable() 
        lookForTable.LookForTable(motionProxy1, portName1)
        #second Nao looks for table
        lookForTable.LookForTable(motionProxy2, portName2)

        #

        goToTable = GoToTable.GoToTable()
        #goToTable.GoToTable(motionProxy, portName1)

        t = threading.Thread(target=goToTable.GoToTable, args=(motionProxy1, portName1))    
        t.start()
        t.join()#for concurrency
        time.sleep(3) 
        #Helper.LiftWithElbowAndShoulders(motionProxy)
        t2 = threading.Thread(target=goToTable.GoToTable, args=(motionProxy2, portName2))
        t2.start()
        t2.join()#for concurrency

        #goToTable = GoToTable.GoToTable()
        #goToTable.GoToTable(motionProxy, portName1)

        print "calling MOveTable class"
        moveTable = MoveTable.MoveTable()
        print "call func"
        moveTable.MoveTableDef(motionProxy1, X, Y, Theta)
        moveTable.MoveTableDef(motionProxy2, X, Y, Theta)
        #    moveTableWithTwoRobots.Main(motionProxy, 0, 2, 0)
        #LookForTable.LookForTable(motionProxy)
        #GoToTable.GoToTable(motionProxy)
        #MoveTable.MoveTable(motionProxy, X, Y, Theta)



