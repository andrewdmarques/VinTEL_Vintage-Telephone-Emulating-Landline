#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# dialer.py (v1.02) decodes the pulses from the phone to determine what
# number was dialed. It generates numbers.txt file that contain the numbers
# dialed. It waits 0.3 seconds before it knows a dialed digit is completely
# returned to home. It waits 4 seconds before it calls a string of numbers
# completely dialed.
##########################################################################
# Load libraries
##########################################################################

import os
import time

##########################################################################
# User input variables
##########################################################################

file_config = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'
# define the directory to monitor
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
dir_dial = '/home/pi/Desktop/VinTEL/Bin/Status/Dial'
file_dial_complete = dir_status + '/dial-complete.txt'
file_dial_number = dir_status + '/Dial/number.txt'

##########################################################################
# Initialize
##########################################################################
print('Initializing dialer.py...')

# initialize variable to count dial-on files
dial_on_count = 0
number_complete = False
time_active1 = time.time()
time_active2 = time.time()
file_deleted = False

##########################################################################
# Run
##########################################################################
print('Running dialer.py...')



# continuously monitor the directory for new files
while True:
    time_active1 = time.time()
    # get the list of files in the directory
    file_list = os.listdir(dir_dial)
    # filter the list to only include files containing "dial-on"
    dial_on_files = [f for f in file_list if "dial-on" in f]
    # if there are no dial-on files, reset the dial-on count and file creation time
    if not dial_on_files:
        dial_on_count = 0
        if file_deleted = False:
            time_inactive = time_active1 - time_active2
            if time_active > 10: # The time since inactive dialing to delete all current logs.
                file_deleted = True
                if os.path.isfile(file_dial_complete):
                    # if it exists, remove the file
                    os.remove(file_dial_complete)
                if os.path.isfile(file_dial_complete):
                    # if it exists, remove the file
                    os.remove(file_dial_complete)
                
        # Determine if a number is complete from being dialed.
        if number_complete == True:
            # Determine the time of the last file that was created.
            sorted_files = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(dir_dial, x)), reverse=True)
            time_last_file = os.path.getctime(os.path.join(dir_dial, sorted_files[0]))
            # Determine the current time.
            time_now = time.time()
            # Calculate how long ago the last file was created.
            time_wait = time_now - time_last_file
            if time_wait > 4:
                # get the current time and format it as a string
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # create the new file and write the current time to the first line
                with open(os.path.join(dir_path, filename), 'w') as f:
                    f.write(current_time + '\n')
            number_complete = False
            
    # if there are dial-on files, check if they were created in rapid succession
    else:
        time_active2 = time.time()
        number_complete = True
        file_deleted = False
        # Determine the time of the last file that was created.
        sorted_files = sorted(file_list, key=lambda x: os.path.getctime(os.path.join(dir_dial, x)), reverse=True)
        time_last_file = os.path.getctime(os.path.join(dir_dial, sorted_files[0]))
        # Determine the current time.
        time_now = time.time()
        
        # Calculate how long ago the last file was created.
        time_wait = time_now - time_last_file
        
        # If it has been more than 0.3 seconds since the last file was generated, then calculate the number that was dialed.
        if time_wait > 0.3:
            dial_on_count = len(dial_on_files) - 1 # This is the length - 1 because there is one extra pulse for each number to be accounted for.
            # The number 0 will create 10 pulses, so we will want to account for this.
            if dial_on_count == 10:
                dial_on_count = 0
            for file in dial_on_files:
                os.remove(os.path.join(dir_dial, file))
            # check if number.txt exists
            if os.path.isfile(os.path.join(dir_dial, "number.txt")):
                # if it exists, append the dial-on count to the first line
                with open(os.path.join(dir_dial, "number.txt"), "r+") as f:
                    contents = f.readlines()
                    contents[0] = contents[0].rstrip() + f"{dial_on_count}\n"
                    f.seek(0)
                    f.writelines(contents)
            else:
                # if it doesn't exist, create it and add the dial-on count to the first line
                with open(os.path.join(dir_dial, "number.txt"), "w") as f:
                    f.write(f"{dial_on_count}\n")
    # wait for 0.1 seconds before checking again
    time.sleep(0.1)

