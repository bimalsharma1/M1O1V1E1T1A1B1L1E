# -*- encoding: UTF-8 -*-

'''Main progrm written by Bimal Sharma to start Nao control'''

import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import ALPhotoCapture
import config
import vision_getandsaveimage
from Utils import DetectColourInImage
import InitialiseHeadAndShoulders
import sys
import os
import moveTowardObjectOfInterest
import thread
import DetectCornersFast
import math
import numpy as np
import cv2
import Logger
import Helper
import BehaviourWalkToLiftRangeOfObject
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
from Queue import Queue
import threading 
import thread
import time
from SimpleBehaviours import MoveToCornerOfObject as m
from SimpleBehaviours import AlignToLongerSideOfObject as a
from Utils import InitialiseNaoRobot
from Utils import ActionHelper as a
from SimpleBehaviours import MoveToOtherSideOfObject as o
from Queue import Queue
exitFlag = 0
print sys.argv
from multiprocessing import Process, Value, Array
from SimpleBehaviours import AlignToLongerSideOfObject as a
from Utils import Helper as h

#Description: Menu to select behaviour to perform
def mainMenu():
    Logger.RenamePreviousFile()
    try:
        print "Select between the tasks below"
        print "Enter 0 for NEW two robot task to move a heavy table"
        print "Enter 1 to look for table"
        print "Enter 2 to go to table"
        print "Enter 3 to move table"
        print "Enter 4 to lift and land table repeatedly"
        print "Enter 5 for single robot task to move a light table"
        print "Enter 6 for two robot task to move a heavy table"
        print "Enter 7 to Look for table"
        print "Enter 8 tMOve to other side"
        print "Enter 9 to align to the middle of table"
        inputChoice = raw_input("Enter your choice: ")

        if ("0" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
        if ("1" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().LookForTable, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().LookForTable, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
        if ("2" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().GoToTable, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().GoToTable, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
        if ("3" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().MoveTable, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().MoveTable, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
        elif ("4" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().LiftLandTableRepeat, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().LiftLandTableRepeat, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
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
            t2 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy,portName1, 0, 2, 0))
            #   threads.append(t)
            t3 = threading.Thread(target=BehaviourWalkToLiftRangeOfObject.LiftObject, args=(motionProxy1,portName2, 0, -2, 0))
            #threads.append(t)
            t2.start()
            t3.start()
            t2.join()#for concurrency
            t3.join()

        elif ("7" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().LookForTable, args=('port1',))
            p0.start()
            p1 = Process(target=MoveTableMain.MoveTableMain().LookForTable, args=('port2',))
            p1.start()
            p0.join()
            p1.join()
        elif ("8" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().AlignToOtherSide, args=('port1',))
            p0.start()
            p0.join()
        elif ("9" in inputChoice):
            p0 = Process(target=MoveTableMain.MoveTableMain().AlignToMiddleOfTable, args=('port1',))
            p0.start()
            p0.join()
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
    print "Enter 4 to move to other side of table"
    print "Enter 9 to initialise robots .."
    inputSubChoice = raw_input("Enter your choice: ")

    initNao1 = InitialiseNaoRobot.InitialiseNaoRobot("port1")
    initNao2 = InitialiseNaoRobot.InitialiseNaoRobot("port2")


    if ("0" in inputSubChoice):
        p0 = Process(target=LookForTable, args=('port1',))
        p0.start()
        p1 = Process(target=LookForTable, args=('port2',))
        p1.start()
        p0.join()
        p1.join()
       
    elif ("1" in inputSubChoice):
        # goToTable1 = GoToTable.GoToTable()
        # goToTable2 = GoToTable.GoToTable()
        t = threading.Thread(target=LookForTable, args=('port1',))    
        t.start()

        t2 = threading.Thread(target=LookForTable, args=('port1',))
        t2.start()
        t2.join()#for concurrency
        t.join()
    elif ("2" in inputSubChoice):
        a.AlignToLongerSideOfObject(motionProxy, portName)   
    elif ("3" in inputSubChoice):
        print "calling MoveTable class"
        moveTable1 = MoveTable.MoveTable()
        moveTable2 = MoveTable.MoveTable()
        print "call func"
        t3 = threading.Thread(target=moveTable1.MoveTableDef, args=(motionProxy1, 0, 1, 0))
        t3.start()
        t4 = threading.Thread(target=moveTable2.MoveTableDef, args=(motionProxy2, 0, -1, 0))
        t4.start()
    elif ("4" in inputSubChoice):
        print "calling MoveToOtherSideOfObject class"

        initNao1 = InitialiseNaoRobot.InitialiseNaoRobot('port1')
        initNao1.wakeUpRobot('port1')
        initNao2 = InitialiseNaoRobot.InitialiseNaoRobot('port2')
        initNao2.wakeUpRobot('port2')

        p0 = Process(target=o.MoveToOtherSideOfObject, args=(initNao1,))
        p0.start()
        p1 = Process(target=o.MoveToOtherSideOfObject, args=(initNao2,))
        p1.start()
        p0.join()
        p1.join()
    elif ("9" in inputSubChoice):
        initNao = InitialiseNaoRobot.InitialiseNaoRobot("port1")
        initNao2 = InitialiseNaoRobot.InitialiseNaoRobot("port2")
