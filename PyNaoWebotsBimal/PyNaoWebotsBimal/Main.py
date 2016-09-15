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
import WalkToPosition 
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
print sys.argv


exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, motionProxy, portName):
        threading.Thread.__init__(self)
        self.motionProxy = motionProxy
        self.portName = portName
    def run(self):
        moveTowardObjectOfInterest.moveTowardObjectOfInterest(self.motionProxy, self.portName)





def main():  

    try:
        print "Select between the tasks below"
        print "Enter 1 for single robot task to move a light table"
        print "Enter 2 for two robot task to move a heavy table"
        print "Enter 3 to select a single behaviour"
        inputChoice = raw_input("Enter your choice: ")

        if ("1" in inputChoice):
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

        elif ("2" in inputChoice):
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






    # moveTowardObjectOfInterest.moveTowardObjectOfInterest,(motionProxy1, 10)
    #try:
    #    thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest,(motionProxy, 10))
    #    thread.start_new_thread(moveTowardObjectOfInterest.moveTowardObjectOfInterest,(motionProxy1, 10))
    #except:
    #    print "error with threading"
    #InitialiseHeadAndShoulders.InitialiseHeadAndShoulders(motionProxy,motionProxy1)
      ## voice text to speech
    #IP = "127.0.0.1"
    #tts = ALProxy("ALTextToSpeech", IP, 9559)
    ## Example: Sends a string to the text-to-speech module
    #print "start speaking"
    #tts.say("Hello Ishaan, I am Nao the  robot, how are you!")
    #print "stop speaking"
    #time.sleep(2)
  

if __name__ == "__main__":
    main()
    