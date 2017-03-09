import numpy as np
import cv2
import argparse
from Utils import DetectColourInImage as d

def main(): 
	img = cv2.imread('TablePicToSelectLongerSide9559.png')
	cv2.imshow("img", img)
	pts1 = np.float32([(164, 228), (340, 208), (638, 359), (316, 451)]) #[(252, 374), (635, 339), (638, 371), (275, 447)])      #[(0, 315), (287, 212), (470, 231), (344, 413)]) 
	warped = four_point_transform(img, pts1)   
	cols, rows = warped.shape[:2]
	M = cv2.getRotationMatrix2D((240,200),90,1)
	dst = cv2.warpAffine(warped,M,(cols,rows)) 
	print warped
	cv2.imshow("Warped", warped)
	cv2.imshow("dst", dst)
	# cv2.imwrite("ImageWarped.png",warped)
	cv2.waitKey(0)





	# image = cv2.imread(args["TablePicToSelectLongerSide9559

	# pts = np.array(eval(args["coords"]), dtype = "float32")
	# warped = four_point_transform(image, pts)
	# cv2.imshow("Original", image)
	# cv2.imshow("Warped", warped)



def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect


def four_point_transform(image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = order_points(pts)   #pts # order_points(pts)
        (tl, tr, br, bl) = rect
    
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
    
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
	print maxWidth,maxHeight
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
	print dst
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(pts, dst)
	print M
        warped = cv2.warpPerspective(image, M, (640, 480))
		# warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
        # return the warped image
        return warped





# # import the necessary packages
# import numpy as np
# from PIL import Image
# import cv2
# import GetCentrePixelPositionOfContour
# import time
# from scipy.spatial import distance as dist
# import Logger
# import config
# import Helper
# import Logger
# from Queue import Queue
# import threading 
# import thread
# import time
# import BehaviourMoveToTopCornerOfObject
# #from ClassesMoveTable import LookForTable


# Logger.Log("MOVE FIRST NAO") 
# portName1 = 'port1'
# motionProxy1 = InitialiseNao.InitialiseFirstNao()
# print "Initialise first nao"

# Logger.Log("MOVE SECOND NAO")    
# portName2 = 'port2'
# motionProxy2 = InitialiseNao.InitialiseSecondNao()
# print "Initialise second nao"
# #q = Queue()

# lookForTable1 = LookForTable.LookForTable() 
# lookForTable1.LookForTable(motionProxy1, portName1)
# #second Nao looks for table
# lookForTable2 = LookForTable.LookForTable() 
# lookForTable2.LookForTable(motionProxy2, portName2)












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
if __name__ == "__main__":
    main()
    