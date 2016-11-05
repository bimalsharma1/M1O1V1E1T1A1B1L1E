# -*- encoding: UTF-8 -*-
# Get an image from NAO. Display it and save it using PIL.
# Python Image Library
from PIL import Image
import numpy as np
from naoqi import ALProxy
import cv2
import vision_definitions
import time
import config
import StringIO
#correct all the names of functions and classes
#give option not to save to file
def showNaoImageTopCam(IP, PORT, FILENAME):
  time.sleep(1)
  #separate proxy from actual call
  camProxy = ALProxy("ALVideoDevice", IP, PORT)
  resolution = 2    # VGA
  colorSpace = 11   # RGB

  cameraCode = vision_definitions.kTopCamera
  print cameraCode
  #camProxy.setActiveCamera("ALVideoDevice",cameraCode)
  videoClient = camProxy.subscribeCamera("python_client",cameraCode, resolution, colorSpace, 5)
  #time.sleep(1)
  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
  naoImage = camProxy.getImageRemote(videoClient)
  camProxy.unsubscribe(videoClient)
  time.sleep(1)
  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
  imageWidth = naoImage[0]
  imageHeight = naoImage[1]
  array = naoImage[6]
  array = np.array(array)
   
  # Create a PIL Image from our pixel array.
  im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
  #im = naoImage
  #config.motionProxyTopImage = cv2.imencode('.png', im)[1].tostring()
  # Save the image.
  im.save(FILENAME + ".png", "PNG")
  #cv2.imencode(".png",im)
  memoryFile = StringIO.StringIO()
  im.save(memoryFile, "PNG")
  memoryFile.write(im.tostring())
  memoryFile.seek(0)
  strMemoryFile = memoryFile.getvalue()
  memoryFile.close()
  time.sleep(1)
  #r, im = cv2.imencode("png",array)
  return strMemoryFile
#  im.show()

 
def showNaoImageBottomCam(IP, PORT, FILENAME):
      time.sleep(2)
      camProxy1 = ALProxy("ALVideoDevice", IP, PORT)
      resolution = 2    # VGA
      colorSpace = 11   # RGB
      cameraCode =  vision_definitions.kBottomCamera 
      print cameraCode
      #camProxy.setActiveCamera("ALVideoDevice",cameraCode)
      videoClient1 = camProxy1.subscribeCamera("python_client",cameraCode, resolution, colorSpace, 5)
      time.sleep(2)
      # Get a camera image.
      # image[6] contains the image data passed as an array of ASCII chars.
      naoImage1 = camProxy1.getImageRemote(videoClient1)
      camProxy1.unsubscribe(videoClient1)
      time.sleep(2)
      # Now we work with the image returned and save it as a PNG  using ImageDraw package.
      # Get the image size and pixel array.
      imageWidth1 = naoImage1[0]
      imageHeight1 = naoImage1[1]
      array1 = naoImage1[6]
      array1 = np.array(array1)
   
      time.sleep(2)
      # Create a PIL Image from our pixel array.
      im1 = Image.fromstring("RGB", (imageWidth1, imageHeight1), array1)
      im1.save(FILENAME + ".png", "PNG")

      memoryFile1 = StringIO.StringIO()
      im1.save(memoryFile1, "PNG")
      memoryFile1.write(im1.tostring())
      memoryFile1.seek(0)
      strMemoryFile1 = memoryFile1.getvalue()
      memoryFile1.close()
 
      time.sleep(2)

      return strMemoryFile1
        #  im.show()


 





