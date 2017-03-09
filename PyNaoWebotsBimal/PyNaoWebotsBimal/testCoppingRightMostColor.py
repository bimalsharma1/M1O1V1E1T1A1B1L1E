import numpy as np
import cv2
import argparse
from Utils import DetectColourInImage as d

def main(): 
	im = cv2.imread('TablePicToSelectLongerSide9559.png')
	x = d.DetectColourInCroppedImageReturnYPos(im, colourToDetect = None)
	cv2.waitKey(0)

if __name__ == "__main__":
    main()
    