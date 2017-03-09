# import the necessary packages
import numpy as np
from PIL import Image
import cv2
import time
from scipy.spatial import distance as dist
import Logger
import config
import datetime

def DetectColour(FILENAME,CAMERANAME, im, colourToDetect = None):
    image = cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)
    
    #print "het height and width" 
    height = np.size(image,0)
    width = np.size(image,1)
    #cv2.imwrite("test1.png",im1)  
    #time.sleep(2)
    objectFound = False
    print "width and  height  of pic"
    print width,height

    contourList=[0 for i in range(5)]
    contourList[4] = [width, height]

    percentOfImageCoveredWithContour = 0
    bottomMostPoint = [0,0]
    bottomMostYPoint = 0

     #colours are in RGB
    lower, upper = GetColourRange(colourToDetect)
    print lower
    print upper 
    try:
    	# find the colors within the specified boundaries and apply
    	# the mask
        mask = cv2.inRange(image, lower, upper)   #mask has black and white image
        cv2.imwrite("mask.png",mask)   #255 is white and 0 is black

        
        try:
            print "BOTTOM MOST POINT BY NP ARRAY"
            #print np.max(np.where(np.max(mask,axis=1)==255))
            bottomMostYPoint = np.max(np.where(np.max(mask,axis=1)==255))
            print bottomMostYPoint
        except Exception as e:
            print "ERROR occurred trying to find largest contour"
            print e
            bottomMostYPoint = 0  
        
        #bottomMostPoint = tuple(mask[mask[:,:,1].argmax()][0])
        #print bottomMostPoint
        output = cv2.bitwise_and(image, image, mask = mask)    #output has found image in the colour
        #cv2.imwrite("output.png",output)
        #    get centre position of colour
        thresh = 90      
        #gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(output,(5,5),0) 
        print "Gaussian blur complete"
        #blur = cv2.GaussianBlur(gray,(5,5),0)  
        edges = cv2.Canny(gray,thresh,thresh*2)  #removed gaussianblur and put gray    
        #cv2.imwrite("blur.png",blur)
        #cv2.imwrite("edges.png",edges)
        #drawing = np.zeros(output.shape,np.uint8)                  # Image to draw the contours
        derp,contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
        #find max contour
        #cnts = contours[0] if imutils.is_cv2() else contours[1]
        #cnt = max(cnts, key=cv2.contourArea)
       
        print "get areas"
        
        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in contours]
        print "find largest contour"
        try:
            if (areas != []):
                print "calc max Index"
                max_index = np.argmax(areas)
                print "calc cnt"
                cnt = contours[max_index]
            else:
                cnt = contours[0]
        except Exception as e:
            print "ERROR occurred trying to find largest contour"
            print e
            return (0,0,False,bottomMostPoint, 0,0,0,0,0)   

      
        #for cnt in contours:   #just removed this loop
        moments = cv2.moments(cnt)                          # Calculate moments
        print "calculating moments"
        if moments['m00']!=0:
            cx = int(moments['m10']/moments['m00'])         # cx = M10/M00
            cy = int(moments['m01']/moments['m00'])         # cy = M01/M00
            areaOfLargestContour = moments['m00']  
            print "MOMENT VALUES"
            print cx, cy, areaOfLargestContour

        try:
            print "finding the bottom most point"
            rect = cv2.minAreaRect(cnt)
            box =  cv2.boxPoints(rect)
            pts = np.int0(box)
            xSorted = pts[np.argsort(pts[:, 0]), :]
            leftMost = xSorted[:2, :]
            rightMost = xSorted[2:, :]
            leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
            (tl, bl) = leftMost
            D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
            (br, tr) = rightMost[np.argsort(D)[::-1], :]

            #the code below replaces the code above to remove depency on bottommost point on drawing a rectangle
            Logger.Log("PRINTING BOTTOMMOST POINTS BELOW:::::")
            Logger.Log(str(tuple(cnt[cnt[:,:,1].argmax()][0]) ))
            Logger.Log(str(bottomMostYPoint))
            bottomMostPoint = tuple(cnt[cnt[:,:,1].argmax()][0])   # removed this as we now get bottom most point directly from the mask to be more accurate
            if (bottomMostYPoint > 0):
                try:
                    lst = list(bottomMostPoint) #convert tuple to list as tuples are immutable
                    Logger.Log(str(lst))
                    lst[1] = bottomMostYPoint  #assign value
                    Logger.Log(str(lst[1]))
                    bottomMostPoint = tuple(lst)
                    Logger.Log(str(bottomMostPoint))
                except Exception as e:
                    Logger.Log(str(e))
            contourList[0] = tuple(cnt[cnt[:,:,0].argmin()][0])   #leftmost
            contourList[1] = tuple(cnt[cnt[:,:,1].argmin()][0])   #topmost
            contourList[2] = tuple(cnt[cnt[:,:,0].argmax()][0])   #rightmost
            contourList[3] = tuple(cnt[cnt[:,:,1].argmax()][0])   #bottomMOst
            #contourList[4] HAS HEIGHT AND WIDTH 
            # Numpy gives coordinates in **(row, column)** format, while OpenCV gives coordinates in **(x,y)** format. So basically the answers will be interchanged. Note that, row = x and column = y.
           

            Logger.Log(str(contourList))
            objectFound = True
            #bottomMostPoint = tuple(cnt[cnt[:,:,1].argmax()][0])
            #print "bottom most y axis"
            #print bottomMostPoint,bottomMostPoint[0],bottomMostPoint[1]
            #if (bottomMostPoint[1] > 0):  #if the bottom most point is more than 60% of picture
                
            #    bottomMostYPoint = bottomMostPoint[1]
            #    print "object found in  picture"

        except Exception as e:
            return (0,0,False,bottomMostPoint, 0,0,0,0,0)            

        #cv2.circle(output,(cx,cy),5,(0,0,255),-1)       
        print "dimensions"
        print cx, cy, objectFound, bottomMostPoint, contourList
        print "all points"
        print bl,br,tl,tr
        return (cx, cy, objectFound, bottomMostPoint, contourList,bl,br,tl,tr)
    except Exception as e:
        print e
        return (0,0,False,bottomMostPoint, 0,0,0,0,0)



def FindObjectPositionInformation(cnt):
    try:
        print "finding the bottom most point"
        bottomMostPoint = tuple(cnt[cnt[:,:,1].argmax()][0])
        print "bottom most y axis"
        print bottomMostPoint,bottomMostPoint[0],bottomMostPoint[1]
        if (bottomMostPoint[1] > 0):  #if the bottom most point is more than 60% of picture
            objectFound = True
            print "object found in  picture" 
        return bottomMostPoint
    except Exception as e:
        print e
        return (0)



def detectColouredObjectWithoutDetails( im, colourToDetect = None):
    image = im
     #colours are in RGB
    lower, upper = GetColourRange(colourToDetect)
    
    print lower
    print upper 
    try:
    	# find the colors within the specified boundaries and apply
    	# the mask
        mask = cv2.inRange(image, lower, upper)   #mask has back and white image
        output = cv2.bitwise_and(image, image, mask = mask)    #output has found image in the colour
        #    get centre position of colour
        thresh = 90      
        gray = cv2.GaussianBlur(output,(5,5),0) 
        print "Gaussian blur complete"
        edges = cv2.Canny(gray,thresh,thresh*2)  #removed gaussianblur and put gray    
        derp,contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    
        #find max contour
        print "find the highest contour"
        topMostYPoint = 0
        # Find the index of the largest contour
        #cntrs = [cv2.contourArea(c) for c in contours]
        if (contours != []):
            for c in contours:
                print "find top most contour"
                topMostPoint = tuple(c[c[:,:,1].argmin()][0])   #topmost
                if(topMostYPoint < topMostPoint[1]):
                    topMostYPoint = topMostPoint[1]
                    print "calc cnt"
                    cnt = c
        else:
            print "error"
            return (False)
      
        x,y,w,h = cv2.boundingRect(cnt)
        print "blue colur values"
        print x,y,w,h
        if (w*h > 10):
            return True
        else:
            return False
    except Exception as e:
        print e
        return False

def GetHeightWidth(FILENAME,CAMERANAME, im, colourToDetect = None):
    image = cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)
    
    #print "het height and width" 
    height = np.size(image,0)
    width = np.size(image,1)

    return height, width


def GetColourRange( colourToDetect = None):
         #colours are in RGB
    if (colourToDetect is  None): # default is blue
        lower_range = np.array([50, 0, 0])
        upper_range = np.array([255, 50, 50])
    elif (colourToDetect.upper() == 'RED'):
        lower_range = np.array([0, 0, 170])
        upper_range = np.array([60, 60, 255])
    elif (colourToDetect.upper() == 'YELLOW'):
        lower_range = np.array([25, 146, 190])
        upper_range = np.array([62, 174, 250])
    elif (colourToDetect.upper() == 'GREY'):
        lower_range = np.array([103, 86, 65])
        upper_range = np.array([145, 133, 128])
    else:
        lower_range = np.array([50, 0, 0])
        upper_range = np.array([255, 50, 50])

    lower = np.array(lower_range, dtype = "uint8")
    upper = np.array(upper_range, dtype = "uint8")
    return lower, upper



# Numpy gives coordinates in **(row, column)** format, 
#while OpenCV gives coordinates in **(x,y)** format. 
#So basically the answers will be interchanged. Note that, row = x and column = y.
def DetectXPos(im, YPixelNumber, startIndex, stopIndex, colourToDetect = None):
    image = cv2.imdecode(np.fromstring(im, dtype='uint8'), cv2.IMREAD_UNCHANGED)
    lower, upper = GetColourRange(colourToDetect)
    XPos= -1
    incrementSize = 1

    try:
    	# find the colors within the specified boundaries and apply
    	# the mask
        mask = cv2.inRange(image, lower, upper)   #mask has black and white image
        Logger.Log("mask sizes")
        height = np.size(mask,0)
        width = np.size(mask,1)
        Logger.Log(str(height))
        Logger.Log(str(width))
         # 0 is black and 255 is white
        #cv2.imshow("croppedRightmost", mask)
        try:
            Logger.Log("Inside: detect XPOS function")
            Logger.Log(str(startIndex))
            Logger.Log(str(stopIndex))
            Logger.Log(str(YPixelNumber))

            previousIndex = -1

            if (stopIndex < startIndex):
                incrementSize = -1
                Logger.Log("Increment size")
                Logger.Log(str(incrementSize))
            
            for XIndex in range(startIndex, stopIndex, incrementSize):
                Logger.Log("Looking for black colour now")
                Logger.Log(str(XIndex))
                Logger.Log(str(YPixelNumber))
                
                colourValue = mask[YPixelNumber, XIndex]
                Logger.Log(str(colourValue))
                print colourValue 
                if(colourValue == 0):  
                    Logger.Log("Found DetectXPOS position x")
                    Logger.Log(str(previousIndex))                     
                    return previousIndex      
                    ####stop as soon as you find a black as you already start at the mid white of the mask
                previousIndex = XIndex
            
            return previousIndex
            Logger.Log("longer Y val not found")
            # print tuple(mask[mask[:,:,0].argmin()][0])
        except Exception as e:
            print "ERROR occurred trying to find pixel value for Y point"
            print e
            return previousIndex

        
    except Exception as e:
        Logger.Log("Error: ")
        Logger.Log(str(e))