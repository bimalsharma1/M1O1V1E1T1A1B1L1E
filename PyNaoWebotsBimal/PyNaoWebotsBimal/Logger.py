import os
from datetime import datetime

def Log( s):
    currentDateTime = "{:%B %d, %Y}".format(datetime.now())
    # Open a file
    fo = open("log.txt",'a') # w for write and a for append
    fo.write("{:%B %d, %Y %H:%M:%S:%f}".format(datetime.now()) + "\t" + s +"\n" );
    # Close opend file
    fo.close()     