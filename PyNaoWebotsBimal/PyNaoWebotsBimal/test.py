# import the necessary packages
import numpy as np
from PIL import Image
import cv2
import GetCentrePixelPositionOfContour
import time
from scipy.spatial import distance as dist
import Logger
import config

image = cv2.imread("naoImageTopCamera.png") #cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)

lower_range = np.array([50, 0, 0])
upper_range = np.array([255, 50, 50])

lower = np.array(lower_range, dtype = "uint8")
upper = np.array(upper_range, dtype = "uint8")
mask = cv2.inRange(image, lower, upper) #mask has back and white image
cv2.imwrite("1.png",mask)
output = cv2.bitwise_and(image, image, mask = mask) #output has found image in the colour
cv2.imwrite("2.png",output)
# get centre position of colour
thresh = 90 
#gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(output,(5,5),0)  
edges = cv2.Canny(gray,thresh,thresh*2) #removed gaussianblur and put gray 
cv2.imwrite("test1.png",edges)


drawing = np.zeros(output.shape,np.uint8)                  # Image to draw the contours
derp,contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    

areas = [cv2.contourArea(c) for c in contours]
if (areas != []):
    max_index = np.argmax(areas)
    cnt = contours[max_index]

#for cnt in contours:   #just removed this loop
moments = cv2.moments(cnt)                          # Calculate moments
if moments['m00']!=0:
    cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
    cy = int(moments['m01']/moments['m00'])         # cy = M01/M00
    areaOfLargestContour = moments['m00']  
    print "MOMENT VALUES"
    print cx, cy, areaOfLargestContour


print "finding the bottom most point"
rect = cv2.minAreaRect(cnt)
box =  cv2.boxPoints(rect)
box = np.int0(box)
pts = box
print rect
print box

contourList=[0 for i in range(5)]

xSorted = pts[np.argsort(pts[:, 0]), :]
leftMost = xSorted[:2, :]
rightMost = xSorted[2:, :]
leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
(tl, bl) = leftMost
D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
(br, tr) = rightMost[np.argsort(D)[::-1], :]
bottomMostPoint = tuple(cnt[cnt[:,:,1].argmax()][0])
contourList[0] = tuple(cnt[cnt[:,:,0].argmin()][0])   #leftmost
contourList[1] = tuple(cnt[cnt[:,:,1].argmin()][0])   #topmost
contourList[2] = tuple(cnt[cnt[:,:,0].argmax()][0])   #rightmost
contourList[3] = bottomMostPoint   #bottomMOst

cv2.drawContours(image,[box],0,(0,0,255),2)
cv2.drawMarker(image, bottomMostPoint,(0,255,0))
cv2.drawMarker(image, contourList[0],(0,255,0))
cv2.drawMarker(image, contourList[1],(0,255,0))
cv2.drawMarker(image,contourList[2],(0,255,0))
cv2.imwrite("test2.png",image)

    #