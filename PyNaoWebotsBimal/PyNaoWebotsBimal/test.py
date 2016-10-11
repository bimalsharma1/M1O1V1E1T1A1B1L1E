# import the necessary packages
import numpy as np
from PIL import Image
import cv2
import GetCentrePixelPositionOfContour
import time
from scipy.spatial import distance as dist
import Logger
import config
import config9559
import Helper

ipAddress1='127.0.0.1'
ipAddress2='127.0.0.1'
port1 = 9557
port2= 9559

#ipList = [ipAddress1+':'+str(port1)]
#config9559.ListOfNaosDetected.append([ipList,"",""])


Helper.AddNao(ipAddress1, port1)

Helper.AddNao(ipAddress2, port2)
print config.Leader

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