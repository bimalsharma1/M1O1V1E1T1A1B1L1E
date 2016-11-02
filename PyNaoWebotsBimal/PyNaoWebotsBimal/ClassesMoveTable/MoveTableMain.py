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
import BehaviourMoveToTopCornerOfObject

class MoveTableMain:
    """description of class"""
    def Main(self):
        Logger.Log("MOVE FIRST NAO") 
        portName1 = 'port1'
        motionProxy1 = InitialiseNao.InitialiseFirstNao()
        print "Initialise first nao"

        Logger.Log("MOVE SECOND NAO")    
        portName2 = 'port2'
        motionProxy2 = InitialiseNao.InitialiseSecondNao()
        print "Initialise second nao"
        #q = Queue()

        lookForTable1 = LookForTable.LookForTable() 
        # lookForTable1.LookForTable(motionProxy1, portName1)
        # #second Nao looks for table
        lookForTable2 = LookForTable.LookForTable() 
        # lookForTable2.LookForTable(motionProxy2, portName2)

        t0 = threading.Thread(target=lookForTable1.LookForTable, args=(motionProxy1, portName1))    
        t0.start()
        t0.join()#for concurrency
        #Helper.LiftWithElbowAndShoulders(motionProxy)
        t1 = threading.Thread(target=lookForTable2.LookForTable, args=(motionProxy2, portName2))
        t1.start()
        t1.join()#for concurrency

        #test
        #BehaviourMoveToTopCornerOfObject.behaviourMoveToTopCornerOfObject(motionProxy1, portName1)
        #BehaviourMoveToTopCornerOfObject.behaviourMoveToTopCornerOfObject(motionProxy2, portName2)

        goToTable1 = GoToTable.GoToTable()
        goToTable2 = GoToTable.GoToTable()
        #goToTable.GoToTable(motionProxy, portName1)
        print "before go to tabkle threaD"
        t = threading.Thread(target=goToTable1.GoToTable, args=(motionProxy1, portName1))    
        t.start()
        #t.join()#for concurrency
        #Helper.LiftWithElbowAndShoulders(motionProxy)
        t2 = threading.Thread(target=goToTable2.GoToTable, args=(motionProxy2, portName2))
        t2.start()
        t2.join()#for concurrency
        t.join()

        #goToTable = GoToTable.GoToTable()
        #goToTable.GoToTable(motionProxy, portName1)

        print "calling MoveTable class"
        moveTable1 = MoveTable.MoveTable()
        moveTable2 = MoveTable.MoveTable()
        print "call func"
        t3 = threading.Thread(target=moveTable1.MoveTableDef, args=(motionProxy1, 0, 1, 0))
        t3.start()
        t4 = threading.Thread(target=moveTable2.MoveTableDef, args=(motionProxy2, 0, -1, 0))
        t4.start()
        
        #moveTable1.MoveTableDef(motionProxy1, 0, 4, 0)  
        #moveTable2.MoveTableDef(motionProxy2, 0, -4, 0)


        #    moveTableWithTwoRobots.Main(motionProxy, 0, 2, 0)
        #LookForTable.LookForTable(motionProxy)
        #GoToTable.GoToTable(motionProxy)
        #MoveTable.MoveTable(motionProxy, X, Y, Theta)



