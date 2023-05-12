#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# audio-selector.py (v1.01) determines what content to play and for how long.
# This script makes the selection for what to play.
##########################################################################
# Load libraries
##########################################################################

import time
from datetime import datetime
import csv
import os

##########################################################################
# User input variables
##########################################################################

config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

##########################################################################
# Initialize
##########################################################################

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']
        if row['variable'] == 'dir_effects':
            dir_effects = row['directory']
        if row['variable'] == 'dir_scripts':
            dir_scripts = row['directory']
            

file_main     = dir_status + '/main-on.txt'
file_hook_on  = dir_status + '/hook-on.txt'
file_hook_off = dir_status + '/hook-off.txt'
file_call_on  = dir_status + '/call-on.txt'
file_player_on = dir_scripts + '/player-on.txt'
file_temp     = dir_scripts + '/temp.py'

##########################################################################
# Run
##########################################################################

# Main on and hook must both be present 
while True:
    if os.path.isfile(file_main):
        if os.path.isfile(file_hook_on):
            # If there is not a call already in process.
            if not os.path.isfile(file_call_on):
                print('Playing dial tone')
                # Begin playing the program.
                with open(file_temp, "w") as job_file:
                    job_file.write("#!/usr/bin/python3\n")
                    job_file.write("import os\n")
                    #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
                    job_file.write("os.system('cvlc --no-xlib --aout=alsa /home/pi/Desktop/VinTEL/Bin/Sound-Effects/dial_tone.mp3')")
                    
                # Indicate to the player script that it should begin playing the program.
                with open(file_player_on, "w") as job_file: # xhost + local: # to give the permissions
                    job_file.write(str(datetime.now()))
                # Indicate that there is a call ongoing.
                with open(file_call_on, "w") as job_file: # xhost + local: # to give the permissions
                    job_file.write(str(datetime.now()))
        else:
            # If the phone is recently placed on the hook, then stop all recordings
            if os.path.isfile(file_hook_off):
                # Get the time of the last modification of the file
                file_time = os.path.getmtime(file_hook_off)
                # Get the current time
                current_time = time.time()
                # Check if the file was modified in the last 5 seconds
                if current_time - file_time < 1:
                    print(f"The file {file_hook_off} was written to in the last 5 seconds.")
                    os.system('killall -9 vlc')
                    os.system('rm -r ' + file_call_on)
                # else:
                    # print(f"The file {file_hook_off} was not written to in the last 5 seconds.")
            else:
                print(f"The file {file_hook_off} does not exist.")
        time.sleep(0.2)
            
    else:
        time.sleep(0.2)

