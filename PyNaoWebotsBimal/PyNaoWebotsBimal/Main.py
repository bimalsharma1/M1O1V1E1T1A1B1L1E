# -*- encoding: UTF-8 -*-

'''Main progrm written by Bimal Sharma to start Nao control'''

import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import InitialiseNao
import ALPhotoCapture
import config
import vision_getandsaveimage
import DetectRedBlueYellowGrey
import InitialiseHeadAndShoulders
import sys
import findObjectOfInterest
import os
import moveTowardObjectOfInterest
import thread
import DetectCornersFast
import math
import DetectRedBlueYellowGrey
import numpy as np
import cv2
import Logger
import Helper
import BehaviourWalkToLiftRangeOfObject
import threading 
import sys
import config
import ClassesMoveTable
from ClassesMoveTable import LookForTable
from ClassesMoveTable import GoToTable
from ClassesMoveTable import GoToOppositeSideOfTable
from ClassesMoveTable import MoveTable
from ClassesMoveTable import LiftTable
from ClassesMoveTable import LandTable
from ClassesMoveTable import PositionToCentreOfTableSide
from ClassesMoveTable import SmallStepSideways
from ClassesMoveTable import MoveTableMain
import Logger
import InitialiseNao
from Queue import Queue
import threading 
import thread
import time
import BehaviourMoveToTopCornerOfObject
from Utils import InitialiseNaoRobot 
from Queue import Queue
exitFlag = 0
print sys.argv
from multiprocessing import Process, Value, Array

def main():  

    try:
        print "Select between the tasks below"
        print "Enter 0 for NEW two robot task to move a heavy table"
        print "Enter 1 for individual behaviours"
        print "Enter 5 for single robot task to move a light table"
        print "Enter 6 for two robot task to move a heavy table"
        print "Enter 7 to select a single behaviour"
        print "Enter 8 to lift and move with table"
        inputChoice = raw_input("Enter your choice: ")

        if ("0" in inputChoice):

            p0 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
            # t0 = threading.Thread(target=MoveTableMain.MoveTableMain().Main, args=('port1',))   
            # t0.start()
            # t1 = threading.Thread(target=MoveTableMain.MoveTableMain().Main, args=('port2',))
            # t1.start()
            # print "start"

        if ("1" in inputChoice):
            PerformIndividualBehaviour()

        elif ("5" in inputChoice):
            Logger.Log("MOVE FIRST NAO") 
            portName1 = 'port1'
            motionProxy = InitialiseNao.InitialiseFirstNao()
      
            t = threading.Thread(target=moveTowardObjectOfInterest.moveTowardObjectOfInterest, args=(motionProxy,portName1))    
            t.start()
            t.join()#for concurrency
            time.sleep(3) 
            Helper.LiftWithElbowAndShoulders(motionProxy)
            t2 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy,portName1, 0, 2, 0))
            t2.start()
            t2.join()#for concurrency

        elif ("6" in inputChoice):
            Logger.Log("MOVE FIRST NAO") 
            portName1 = 'port1'
            motionProxy = InitialiseNao.InitialiseFirstNao()

            Logger.Log("MOVE SECOND NAO")    
            portName2 = 'port2'
            motionProxy1 = InitialiseNao.InitialiseSecondNao()


           # #moveTowardObjectOfInterest.moveTowardObjectOfInterest(motionProxy, portName1)
           # #moveTowardObjectOfInterest.moveTowardObjectOfInterest(motionProxy1, portName2)
      
           # #thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest,(motionProxy,portName1,))    
           # #thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest,(motionProxy1,portName2,))
        
           # ## Create new threads
           # #thread1 = myThread(motionProxy,portName1)
           # #thread2 = myThread(motionProxy1,portName2)

           # ## Start new Threads
           # #thread1.run()
           # #thread2.run()

      
            t = threading.Thread(target=moveTowardObjectOfInterest.moveTowardObjectOfInterest, args=(motionProxy,portName1))
            #   threads.append(t)
            t1 = threading.Thread(target=moveTowardObjectOfInterest.moveTowardObjectOfInterest, args=(motionProxy1,portName2))
            #threads.append(t)
            t.start()
            t1.start()
            t.join()#for concurrency
            t1.join()

            time.sleep(3) 
            Helper.LiftWithElbowAndShoulders(motionProxy)
            Helper.LiftWithElbowAndShoulders(motionProxy1)


           # time.sleep(3)
           # print ("LIFT TABLE")
           # print ("LIFT TABLE")
           # print ("LIFT TABLE")
           # print ("LIFT TABLE")


            t2 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy,portName1, 0, 2, 0))
            #   threads.append(t)
            t3 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy1,portName2, 0, -2, 0))
            #threads.append(t)
            t2.start()
            t3.start()
            t2.join()#for concurrency
            t3.join()
            #BehaviourWalkToLiftRangeOfObject.LiftObject(motionProxy, portName1, 0, 2, 0)
            #BehaviourWalkToLiftRangeOfObject.LiftObject(motionProxy1, portName2, 0, -2, 0)
  
        
            #thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest(motionProxy,portName,))    
           # thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest(motionProxy1,portName,))
        elif ("7" in inputChoice):
            Logger.Log("MOVE FIRST NAO") 
            portName1 = 'port1'
            motionProxy = InitialiseNao.InitialiseFirstNao()

            Logger.Log("MOVE SECOND NAO")    
            portName2 = 'port2'
            motionProxy1 = InitialiseNao.InitialiseSecondNao()

            #time.sleep(3) 
            #Helper.LiftWithElbowAndShoulders(motionProxy)
            #Helper.LiftWithElbowAndShoulders(motionProxy1)

            t2 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy,portName1, 0, 4, 0))
            #   threads.append(t)
            t3 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy1,portName2, 0, -4, 0))
            #threads.append(t)
            t2.start()
            t3.start()
            t2.join()#for concurrency
            t3.join()
            #BehaviourWalkToLiftRangeOfObject.LiftObject(motionProxy, portName1, 0, 2, 0)
            #BehaviourWalkToLiftRangeOfObject.LiftObject(motionProxy1, portName2, 0, -2, 0)
  
        else:
            print "Coming soon!"
        
    except Exception as e:
        print e
        ##kill processes that have not stopped so cleanup
        #os.system("taskkill /F /im hal.exe")
        #os.system("taskkill /F /im hal.exe")
        #os.system("taskkill /F /im naoqi-bin.exe")
        #os.system("taskkill /F /im naoqi-bin.exe")
        #os.system("taskkill /F /im naoqisim.exe")
        #os.system("taskkill /F /im naoqisim.exe")


def PerformIndividualBehaviour():
    print "Select the individual behaviour below and press enter"
    print "Enter 0 to Look for Table"
    print "Enter 1 to go to table"
    print "Enter 2 to go to longer side of table"
    print "Enter 3 to move table"
    print "Enter 9 to initialise robots .."
    inputSubChoice = raw_input("Enter your choice: ")

    initNao1 = InitialiseNaoRobot.InitialiseNaoRobot("port1")
    initNao2 = InitialiseNaoRobot.InitialiseNaoRobot("port2")


    if ("0" in inputSubChoice):
        lookForTable1 = LookForTable.LookForTable(initNao1.camProxy) 
        # lookForTable1.LookForTable(motionProxy1, portName1)
        # #second Nao looks for table
        lookForTable2 = LookForTable.LookForTable(initNao2.camProxy) 
        # lookForTable2.LookForTable(motionProxy2, portName2)
        motionProxy1 = initNao1.motionProxy # InitialiseNaoRobot.InitialiseNaoRobot.motionProxy
        portName1 = 'port1'
        print "thread start a"
        t0 = threading.Thread(target=LookForTable1.LookForTable, args=(initNao1.camProxy))    
        t0.start()
        t0.join()

        motionProxy2 = initNao2.motionProxy# InitialiseNaoRobot.InitialiseNaoRobot.motionProxy
        portName2 = 'port2'
        t1 = threading.Thread(target=LookForTable2.LookForTable, args=(initNao2.camProxy))
        t1.start()
        t1.join()#for concurrency
    elif ("1" in inputSubChoice):
        goToTable1 = GoToTable.GoToTable()
        goToTable2 = GoToTable.GoToTable()
        t = threading.Thread(target=goToTable1.GoToTable, args=(motionProxy1, portName1))    
        t.start()

        t2 = threading.Thread(target=goToTable2.GoToTable, args=(motionProxy2, portName2))
        t2.start()
        t2.join()#for concurrency
        t.join()
    elif ("2" in inputSubChoice):
        # BehaviourMoveToCornerOfObject.behaviourMoveToCornerOfObject(motionProxy, portName)
        BehaviourAlignToLongerSideOfObject.behaviourAlignToLongerSideOfObject(motionProxy, portName)   
    elif ("3" in inputSubChoice):
        print "calling MoveTable class"
        moveTable1 = MoveTable.MoveTable()
        moveTable2 = MoveTable.MoveTable()
        print "call func"
        t3 = threading.Thread(target=moveTable1.MoveTableDef, args=(motionProxy1, 0, 1, 0))
        t3.start()
        t4 = threading.Thread(target=moveTable2.MoveTableDef, args=(motionProxy2, 0, -1, 0))
        t4.start()
    elif ("9" in inputSubChoice):
        initNao = InitialiseNaoRobot.InitialiseNaoRobot("port1")
        initNao2 = InitialiseNaoRobot.InitialiseNaoRobot("port2")

if __name__ == "__main__":
    main()
    