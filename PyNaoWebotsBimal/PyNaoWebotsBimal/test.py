# import the necessary packages
import numpy as np
from PIL import Image
import cv2
import GetCentrePixelPositionOfContour
import time
from scipy.spatial import distance as dist
import Logger
import config
import Helper
import Logger
import InitialiseNao
from Queue import Queue
import threading 
import thread
import time
import BehaviourMoveToTopCornerOfObject
#from ClassesMoveTable import LookForTable


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
lookForTable1.LookForTable(motionProxy1, portName1)
#second Nao looks for table
lookForTable2 = LookForTable.LookForTable() 
lookForTable2.LookForTable(motionProxy2, portName2)












# ipAddress1='127.0.0.1'
# ipAddress2='127.0.0.1'
# port1 = 9557
# port2= 9559

# #ipList = [ipAddress1+':'+str(port1)]
# #config9559.ListOfNaosDetected.append([ipList,"",""])


# Helper.AddNao(ipAddress1, port1)

# Helper.AddNao(ipAddress2, port2)
# print config.Leader

#idList.insert(ipAddress1)
#ipList = ipAddress2+':'+str(port2)
#print ipList
#print max(ipList)

#ipList2 = ipAddress2+':'+str(port2)
#config9559.ListOfNaosDetected.append([ipList2,"",""])


#print "List values"
#print config9559.ListOfNaosDetected
#print "max list value for leader"
#config.Leader = max(sublist[0] for sublist in config9559.ListOfNaosDetected)
#print config.Leader

#ipAddress1.split('.') 
#LastSubnet =  ipAddress1.split('.')
#print LastSubnet[3]


#for number in the_count:
#    print "This is count %d" % number