#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# dialer.py (v1.00) decodes the pulses from the phone to determine what
# number was dialed. It generates numbers.txt file that contain the numbers
# dialed.
##########################################################################
# Load libraries
##########################################################################

import os
import time
from datetime import datetime

##########################################################################
# User input variables
##########################################################################

file_config = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'
# define the directory to monitor
dir_to_monitor = '/home/pi/Desktop/VinTEL/Bin/Status/Dial'

##########################################################################
# Initialize
##########################################################################
print('Initializing dialer.py...')

##########################################################################
# Run
##########################################################################
print('Running dialer.py...')

# initialize variables to track file creation times
last_file_time = 0
current_file_time = 0
# initialize variable to count dial-on files
dial_on_count = 0

# continuously monitor the directory for new files
while True:
    # get the list of files in the directory
    file_list = os.listdir(dir_to_monitor)
    # filter the list to only include files containing "dial-on"
    dial_on_files = [f for f in file_list if "dial-on" in f]
    # if there are no dial-on files, reset the dial-on count and file creation time
    if not dial_on_files:
        dial_on_count = 0
        last_file_time = 0
    # if there are dial-on files, check if they were created in rapid succession
    else:
        # get the creation time of the most recent dial-on file
        current_file_time = os.path.getctime(os.path.join(dir_to_monitor, dial_on_files[-1]))
        # if there was a 0.5 second pause between file creations, count the dial-on files and remove them
        if current_file_time - last_file_time > 2:
            dial_on_count = len(dial_on_files)
            for file in dial_on_files:
                os.remove(os.path.join(dir_to_monitor, file))
            # check if number.txt exists
            if os.path.isfile(os.path.join(dir_to_monitor, "number.txt")):
                # if it exists, append the dial-on count to the first line
                with open(os.path.join(dir_to_monitor, "number.txt"), "r+") as f:
                    contents = f.readlines()
                    contents[0] = contents[0].rstrip() + f" {dial_on_count}\n"
                    f.seek(0)
                    f.writelines(contents)
            else:
                # if it doesn't exist, create it and add the dial-on count to the first line
                with open(os.path.join(dir_to_monitor, "number.txt"), "w") as f:
                    f.write(f"{dial_on_count}\n")
        # update the last file creation time
        last_file_time = current_file_time
    # wait for 0.1 seconds before checking again
    time.sleep(0.1)

