# import the necessary packages
import numpy as np
import cv2
from scipy.spatial import distance as dist
import math
import Logger
#meters per pixel
metersPerPixel = 320 ##assuming 100 pixels = 1 meter....need to work on this

def GetTurnAngleAndWalkDistanceWhenCloserToObject(FILENAME,im):
    rectangle = FindRectangleAndPlot(FILENAME, im)
    angleToTurn,distanceToWalk, bottomMostPoint,longerSide = order_rectangle_points_and_get_longer_side(rectangle)
    return angleToTurn,distanceToWalk,longerSide


def FindRectangleAndPlot(FILENAME, im):
    #Detect corners  
    #FILENAME="2.png"
    # load the image
    #image = cv2.imread(FILENAME)
    #motionProxyTopImage=image

    image = cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)

  #  cv2.imshow("orig", image)
    #image = cv2.medianBlur(image,5) 
    # THE COLOURS ARE IN RGB
    lower_blue = np.array([50, 0, 0])
    upper_blue = np.array([255, 50, 50])

    # loop over the boundaries
    #    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
    lower = np.array(lower_blue, dtype = "uint8")
    upper = np.array(upper_blue, dtype = "uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    maskWidth, maskHeight = mask.shape[:2]
  
    #this blur keeps rectangle outside the table boundary, if you remove, it will draw the rectangle inside the table top
    mask = cv2.GaussianBlur(mask,(5,5),0)
    #cv2.imshow("mask ", mask)
    ret,thresh = cv2.threshold(mask,255,255,255)
    img,contours,hierarchy = cv2.findContours(thresh,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.CHAIN_APPROX_SIMPLE)
    #cnt = contours[0]
    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]

    #draw rectangle that is aligned with picture
    rect = cv2.minAreaRect(cnt)
    #area = cv2.contourArea(cnt)
    #perimeter = cv2.arcLength(cnt,True)
  
    #print "rectangle coordinates"
    #print rect
    box =  cv2.boxPoints(rect)
    #print "box coor"
    #print box
    box = np.int0(box)
    #if negative value for rectangke point then set to 0
    #for i in range(len(box)):
    #    for j in range(len(box[i])):
    #        if box[i][j] <= 0:
    #            box[i][j]=1
    cv2.drawContours(image,[box],0,(0,0,255),2)
    cv2.imwrite("boundingRectangle.png",image)
    #cv2.imshow("bounding", image)

    #now get the rectangle and calculate turn angle and distance and direction
    #rawbox, longSideLeftPoint,longSideRightPoint = order_rectangle_points_and_get_longer_side(rawbox)
    print "raw data without resetting negative values to 1"
    print box

    return box

   


def order_rectangle_points_and_get_longer_side(pts):
    bottomMostPoint = 0
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]
    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]
    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost
    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    #The leftMost  points will thus correspond to the top-left 
    #and bottom-left points while rightMost  will be our top-right and bottom-right points 
    #find distances between two points OR hypotenuse
    
    #if the Y point of bl is greater than the Y point of br then bottom most point is bl
    if (bl[1] > br[1]):
        bottomMostPoint = bl[0]
        hypotLeft=math.hypot(abs(bl[0]-tl[0]), abs(bl[1]-tl[1]))
        hypotRight=math.hypot(abs(bl[0]-br[0]), abs(bl[1]-br[1])) 
        print "left and right hypot values"
        print hypotLeft, hypotRight
         #if left side is longer
        if (abs(hypotLeft) > abs(hypotRight)):
            longerSide = "LEFT"
            longSideLeftPoint = tl
            longSideRightPoint = bl
            #calc angle to turn
            x, y = GetDistanceBetweenTwoPoints(bl, tl)
            angleToTurn = -GetAngleToTurn(x,hypotLeft)
            print "left bl tl"
            print x, y, hypotLeft
            distanceToWalk =  hypotLeft/metersPerPixel ##assuming 100 pixels = 1 meter....need to work on this
        else:
            longerSide = "RIGHT"
            longSideLeftPoint = bl
            longSideRightPoint = br
            #calculate turn angle
            x, y = GetDistanceBetweenTwoPoints(bl, br)
            angleToTurn = GetAngleToTurn(x,hypotRight)
            print "right bl br"
            print  x, y, hypotRight
            distanceToWalk = -1 * hypotRight/metersPerPixel
    else:  #else bottom most point is br
        bottomMostPoint = br[0]
        hypotLeft=math.hypot(abs(bl[0]-br[0]), abs(bl[1]-br[1]))
        hypotRight=math.hypot(abs(br[0]-tr[0]), abs(br[1]-tr[1])) 
        print "left and right hypot values"
        print hypotLeft, hypotRight
         #if left side is longer
        if (abs(hypotLeft) > abs(hypotRight)):
            longerSide = "LEFT"
            longSideLeftPoint = bl
            longSideRightPoint = br
            #calc angle to turn
            x, y = GetDistanceBetweenTwoPoints(bl, br)
            angleToTurn = GetAngleToTurn(x,hypotLeft)
            print "left bl br"
            print x, y, hypotLeft
            distanceToWalk =  hypotLeft/metersPerPixel ##assuming 100 pixels = 1 meter....need to work on this
        else:
            longerSide = "RIGHT"
            longSideLeftPoint = br
            longSideRightPoint = tr
            #calculate turn angle
            x, y = GetDistanceBetweenTwoPoints(br, tr)
            angleToTurn = -GetAngleToTurn(x,hypotRight)
            print "right br tr"
            print  x, y, hypotRight
            distanceToWalk = -1 * hypotRight/metersPerPixel


    print "turn angle and distance to walk " 
    print angleToTurn,distanceToWalk

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return  angleToTurn,distanceToWalk,bottomMostPoint,longerSide


def GetAngleToTurn (x, h):
    #when right angle is on bottom left
    #A is on left, B is on the bottom
    #C is the hypotenuse
    turnAngleInRadians = math.acos(x/ h)
    print "turn angle in radians"
    print x, h, turnAngleInRadians, math.degrees(turnAngleInRadians)
    return turnAngleInRadians

def GetDistanceBetweenTwoPoints(a, b):
    print a,b
    X = a[0] - b[0]
    Y = a[1] - b[1]
    #to avoid divide by 0 error
    if (X == 0):
        X = 1
    if (Y == 0):
        Y = 1
    print "distance between X and Y points" 
    print abs(X), abs(Y)
    return abs(X), abs(Y)


