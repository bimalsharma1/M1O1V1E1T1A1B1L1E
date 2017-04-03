import os
import config
from datetime import datetime

def Log( s):
    currentDateTime = "{:%B %d, %Y}".format(datetime.now())
    # Open a file
    fo = open("log.txt",'a') # w for write and a for append
    fo.write("{:%B %d, %Y %H:%M:%S:%f}".format(datetime.now()) + "\t" + config.loggingId + "\t" + s +"\n" );
    # Close opend file
    fo.close()
def RenamePreviousFile():
    currentDateTime = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    newFileName = "zlog"+currentDateTime+".txt"
    if (os.path.isfile("log.txt")):
        os.rename("log.txt",newFileName)