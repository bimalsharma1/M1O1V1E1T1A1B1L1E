import numpy as np
import cv2
import argparse
from Utils import DetectColourInImage as d
import Logger as l

def getPerspectiveTransformFromMemory(im, corners):
    img = cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)
    pts1 = np.float32(corners)      #[(0, 315), (287, 212), (470, 231), (344, 413)]
    warped, width, height  = four_point_transform(img, pts1)
    l.Log("print of warped")
    l.Log(str(warped))
    print warped
    l.Log("Width and height from get perspective")
    l.Log(str(width))
    l.Log(str(height))
#     cv2.imshow("Warped", warped)
# 	cv2.imwrite("ImageWarped.png",warped)
# 	cv2.waitKey(0)
    return warped # width, height 
	# cv2.waitKey(0)

def getPerspectiveTransformFromMFile(imgFileName, corners):  
	img = cv2.imread(imgFileName + '.png')   #png
	pts1 = np.float32(corners)    #np.float32([(0, 315), (287, 212), (470, 231), (344, 413)]) 
        l.Log("start to get 4 point transform")
	warped, width, height = four_point_transform(img, pts1)    
	print warped
	# cv2.imshow("Warped", warped)
	cv2.imwrite("ImageWarped.png",warped)
	cv2.waitKey(0)

def rotateImage(img, degreesToRotate, xPosToRotate, yPosToRotate): #+ve dgrees is counterclockwise
        l.Log("rotating image")
        cols, rows = img.shape[:2]
        l.Log("get img cols and rows")
	M = cv2.getRotationMatrix2D((xPosToRotate,yPosToRotate),degreesToRotate,1)
	dst = cv2.warpAffine(img,M,(cols,rows)) 
        cv2.imwrite("dst.png", dst)
	# print img
	# cv2.imshow("img", img)
        return dst
	# cv2.imshow("img1", dst)

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
        warped = cv2.warpPerspective(image, M, (640, 480)) #maxWidth, maxHeight
    
        #since the transform see from the right of the image,rotate the image left by 90 degrees to see from the robots perspective
        
        
        # return the warped image
        return warped, maxWidth, maxHeight
