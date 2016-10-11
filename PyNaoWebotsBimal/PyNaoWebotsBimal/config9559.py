# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 21:28:02 2016

@author: bimal
"""

ports = dict(
    port1 = 9557,
    port2 = 9559,
    )
ipAddress = '127.0.0.1'

InitialLongerSideOfTable = ""

#collection of all Nao robots detected, can make multi dim by adding ListOfNaosDetected.append([id,leader])
#keep 4 dim list ListOfNaosDetected.append([ipAddress+Port, [MsgReceived], [MsgSent]])
#to find index myList.index("revolves")
ListOfNaosDetected = [] 
Leader = ""

#def init():
#global InitialLongerSideOfTable