#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# motion-controller.py (v1.01) reads the data from the motion sensor. If
# there is motion detected, and the switch for motion activated skit is on,
# and it has been more than 5 minutes (as an example) since the last
# detection of motion, then give it a 1/3 random chance that there will 
# be an unattended incomming call prompted.
##########################################################################
# Load libraries
##########################################################################

import os
import csv
import time
import RPi.GPIO as GPIO
import random # To determine if the motion should randomly call a new skit.
from datetime import datetime # For writing the files that motion was detected.

##########################################################################
# User input variables
##########################################################################

time_of_inactivity = 5                # Time (minutes) that the system would have to wait without detecting motion before there is a chance of an incoming call with newly detected motion.
probability_of_incoming_call = 1/3    # Probability (0-1) that the newly detected motion prompts an incoming call. Values of 1 would result in a call every time there is newly detected motion.

##########################################################################
# Inititalization
##########################################################################

# Open the configuration file and read the data
config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['description'] == 'motion sensor':
            sensor_motion = int(row['pin'])
        elif row['variable'] == 'dir_status':
            dir_status = row['directory']


file_motion   = dir_status + '/detected-motion.txt' # The file that indicates that motion was detected.
file_motion_on = dir_status + '/motion-on.txt' 
file_call_initiated_unattended  = dir_status + '/call-initiated-unattended.txt' # The file that indicates that the motion sensor triggered a call to be made.
system_working_file = dir_status + '/system-working.txt'
file_main_on = dir_status + '/main-on.txt'

# Set up the input and output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_motion, GPIO.IN)

# Reset the environment the first time the skit is set to run.
if os.path.isfile(file_motion):
    os.remove(file_motion)
if os.path.isfile(file_call_initiated_unattended):
    os.remove(file_call_initiated_unattended)  

##########################################################################
# Run
##########################################################################

# Main on and motion sensor activeted incoming calls must be on 
while True:
    if os.path.isfile(file_main_on):        # If the main switch is on
        if os.path.isfile(file_motion_on):  # If the switch to enable motin detected initiated calls is on.
            #if GPIO.input(sensor_motion):
            if os.path.isfile(file_motion):
                # Motion detected
                #print('Motion detected!')
                # Write motion detection file
#                 with open(file_motion, "w") as job_file: # xhost + local: # to give the permissions
#                     job_file.write(str(datetime.now()))
#                     print('Motion detection file written!')  
                # Check time since last motion detection file was created
                if not os.path.exists(file_motion) or (time.time() - os.path.getmtime(file_motion)) > (time_of_inactivity*60):
                    num_rand = random.random()
                    # Last detection was more than 5 minutes ago, so initiate skit with 1/3 chance
                    if num_rand < probability_of_incoming_call:
                        print(num_rand)
                        with open(file_call_initiated_unattended, "w") as job_file: # xhost + local: # to give the permissions
                            job_file.write(str(datetime.now()))
                            #print('Initiated skit unattended!')    
            else:
                #print('No motion detected')
        else:
            if os.path.isfile(file_call_initiated_unattended):
                os.remove(file_call_initiated_unattended)     
    else:
        if os.path.isfile(file_call_initiated_unattended):
            os.remove(file_call_initiated_unattended)
                
        
    time.sleep(0.5)
