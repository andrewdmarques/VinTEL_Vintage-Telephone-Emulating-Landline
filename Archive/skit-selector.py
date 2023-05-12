#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# skit-selector.py (v1.00) This searches for motion detected or docent-
# initiated call and then randomly selects an appropriate interaction.
# There cannot be an ongoing call, it will ignore a message in that case.
##########################################################################
# Load libraries
##########################################################################

import time
from datetime import datetime
import csv
import os
import re
import random               # For selecting a random file to play from.

##########################################################################
# User input variables
##########################################################################

config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

##########################################################################
# Initialize
##########################################################################
print('Initializing')

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']
        elif row['variable'] == 'dir_effects':
            dir_effects = row['directory']
        elif row['variable'] == 'dir_scripts':
            dir_scripts = row['directory']
        elif row['variable'] == 'dir_audio':
            dir_audio = row['directory']
        elif row['variable'] == 'dir_skits':
            dir_skits = row['directory']

file_main     = dir_status + '/main-on.txt'       # The file that indicates the main switch is toggled to the on position.
file_hook_on  = dir_status + '/hook-on.txt'       # The file that indicates the handset was picked up, the hook is toggled to the on position.
file_hook_off = dir_status + '/hook-off.txt'      # The file that indicates the handset was placed down, the hook is toggled to the off position.
file_call_on  = dir_status + '/call-on.txt'       # The file that indicates there is already a call in progress.
file_dialed   = dir_status + '/dial-complete.txt' # The file that indicates that a number is completed being dialed.
file_number   = dir_status + '/Dial/number.txt'   # The file containing the dialed numbers on the first line.
file_skit_on  = dir_status + '/skit-on.txt'       # The file that indicates that a skit should be played, beginning skit-player.py.
file_call_initiated  = dir_status + '/call-initiated.txt' # The file that indicates that the docent triggered a call to be made.
file_call_initiated_unattended  = dir_status + '/call-initiated-unattended.txt' # The file that indicates that the motion sensor triggered a call to be made.
file_player_on = dir_scripts + '/player-on.txt'   # The file that indicates that that vlc should be activated and begin playing the selected audio file.
file_temp      = dir_scripts + '/temp.py'         # The file that contains the commands to play the specified audio file.
file_skit_wait = dir_status + '/skit-wait.txt'    # The file that indicates that a skit should waint until action is performed.
action         = 'unknown'                        # This must be reset between file types, it is used to trigger search for input type (dial, hook, audio, coin).

##########################################################################
# Run
##########################################################################
print('Running...')

# Main on and the skit file must be present 
while True:
    if os.path.isfile(file_main):
        if os.path.isfile(file_call_initiated):
            
            # Time to wait before initiating a call from the time that the button is pushed.
            time.sleep(5)
            
            # Remove the initiated call.
            os.system('rm -r ' + file_call_initiated)
            
            # If there is not an ongoing call already.
            if not os.path.isfile(file_call_on):
                # Report that the skit is ongoing.
                with open(file_call_on, "w") as job_file: # xhost + local: # to give the permissions
                    job_file.write(str(datetime.now()))
                
                # Select from one of the "incoming_with_docent" skits.
                # Get all CSV files in the directory that start with "incoming_call_docent"
                csv_files = [f for f in os.listdir(dir_audio) if f.startswith("incoming_call") and f.endswith(".csv")]
                if csv_files:  # check if the list is not empty
                    # Randomly select one of the CSV files
                    file_skit = random.choice(csv_files)
                    
                    # Indicate to the skit script that should be played.
                    with open(file_skit_on, "w") as job_file: # xhost + local: # to give the permissions
                        job_file.write(file_skit)
        
        # Determine the skit to play if it is activated by the motion sensor.
        if os.path.isfile(file_call_initiated_unattended):
            
            # Time to wait before initiating a call from the time that the button is pushed.
            time.sleep(10)
            
            # Remove the initiated call.
            os.system('rm -r ' + file_call_initiated_unattended)
            
            # If there is not an ongoing call already.
            if not os.path.isfile(file_call_on):
                
                # Select from one of the "incoming_with_docent" skits.
                # Get all CSV files in the directory that start with "incoming_call_docent"
                csv_files = [f for f in os.listdir(dir_audio) if f.startswith("incoming_call_unattended") and f.endswith(".csv")]
                if csv_files:  # check if the list is not empty
                    # Randomly select one of the CSV files
                    file_skit = random.choice(csv_files)
                    # Indicate to the skit script that should be played.
                    with open(file_skit_on, "w") as job_file: # xhost + local: # to give the permissions
                        job_file.write(file_skit)

    time.sleep(0.2)
    
