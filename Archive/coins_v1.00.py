#!/usr/bin/python
##########################################################################
# Description
##########################################################################
# coins.py (v1.00) determines what coins were placed into the phone. After
# controller.py makes the files, then this script renames the files to have
# a time stamp added to the file name, and detects if the 25 cent and 10
# cent sensors went off, then this should just be a 10 cent. 
##########################################################################
# Load libraries
##########################################################################

import os
import time
from datetime import datetime

##########################################################################
# Initialize
##########################################################################


file_5 = '/home/pi/Desktop/VinTEL/Bin/Status/detected-5-cent.txt'
file_10 = '/home/pi/Desktop/VinTEL/Bin/Status/detected-10-cent.txt'
file_25 = '/home/pi/Desktop/VinTEL/Bin/Status/detected-25-cent.txt'

##########################################################################
# Run
##########################################################################

while True:
    if os.path.exists(file_5):
        os.rename(file_5, file_5[:-4] + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
    if os.path.exists(file_10):
        file_10_time = os.path.getctime(file_10)
        os.rename(file_10, file_10[:-4] + '_' + datetime.fromtimestamp(file_10_time).strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
        time.sleep(0.75)
        if os.path.exists(file_25):
            file_25_time = os.path.getctime(file_25)
            if (file_10_time - file_25_time) < 0.75:
                os.remove(file_25)
    if os.path.exists(file_25):
        os.rename(file_25, file_25[:-4] + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
    time.sleep(0.1)





