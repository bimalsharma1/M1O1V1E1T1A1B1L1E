'''Main progrm written by Bimal Sharma to start Nao control'''
import almath as m # python's wrapping of almath
from naoqi import ALProxy
import time
import MoveTable
import config
import sys
import os
import math
import subprocess
def main():

 #kill processes that have not stopped so cleanup
        os.system("taskkill /F /im hal.exe")
        os.system("taskkill /F /im hal.exe")
        os.system("taskkill /F /im naoqi-bin.exe")
        os.system("taskkill /F /im naoqi-bin.exe")
        os.system("taskkill /F /im naoqisim.exe")
        os.system("taskkill /F /im naoqisim.exe")
        os.system("taskkill /F /im webots.exe")

        subprocess.call(['C:\\Program Files (x86)\\Webots\\Webots.exe'])

  

if __name__ == "__main__":
    main()
    