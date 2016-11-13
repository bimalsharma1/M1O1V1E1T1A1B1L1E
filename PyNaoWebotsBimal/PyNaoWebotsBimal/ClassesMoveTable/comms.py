

InitialLongerSideOfTable = ""

#collection of all Nao robots detected, can make multi dim by adding ListOfNaosDetected.append([id,leader])
#keep 4 dim list ListOfNaosDetected.append([ipAddress+Port, [MsgReceived], [MsgSent]])
#to find index myList.index("revolves")
ListOfNaosDetected = [] 

MessagesSent = [] 
MessagesReceived = []
#def init():
#global InitialLongerSideOfTable
ReadyToLift = False
LeaderConfirmedReadyToLift = False