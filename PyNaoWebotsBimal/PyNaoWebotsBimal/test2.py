# -*- encoding: UTF-8 -*-

'''Main progrm written by Bimal Sharma to start Nao control'''

import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import sys
import os



name = raw_input("Hi what is your name?")
print "Hi " + name

age = 0 
age = int(raw_input("Hi what is your age?"))
yearBorn = 2016 - age
print "Your were born in  " + str(yearBorn)
if(age > 12 and age <= 19):
    print "You are a teenager"
elif(age> 19 and age < 30):
    print "you are a 20s man"
else: 
    print "you are not a teenager"

        # print "Hi What is your name?"
        # print "Enter 0 for NEW two robot task to move a heavy table"
        # print "Enter 1 for individual behaviours"
        # print "Enter 5 for single robot task to move a light table"
        # print "Enter 6 for two robot task to move a heavy table"
        # print "Enter 7 to select a single behaviour"
        # print "Enter 8 to lift and move with table"
        # inputChoice = raw_input("Enter your choice: ")

        # if ("0" in inputChoice):

        #     p0 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port1',))
        #     p0.start()
        #     p1 = Process(target=MoveTableMain.MoveTableMain().Main, args=('port2',))
        #     p1.start()
        #     p0.join()
        #     p1.join()