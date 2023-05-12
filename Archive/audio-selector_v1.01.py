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
import re

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
        if row['variable'] == 'dir_effects':
            dir_effects = row['directory']
        if row['variable'] == 'dir_scripts':
            dir_scripts = row['directory']
        if row['variable'] == 'dir_audio':
            dir_audio = row['directory']
        if row['variable'] == 'dir_skits':
            dir_skits = row['directory']
 
file_number   = dir_status + '/Dial/number.txt'
file_main     = dir_status + '/main-on.txt'
file_hook_on  = dir_status + '/hook-on.txt'
file_hook_off = dir_status + '/hook-off.txt'
file_call_on  = dir_status + '/call-on.txt'
file_dialed   = dir_status + '/dial-complete.txt'
file_player_on = dir_scripts + '/player-on.txt'
file_temp     = dir_scripts + '/temp.py'

dial_tone = False
call_in_progress = False

##########################################################################
# Run
##########################################################################
print('Running...')

# Main on and hook must both be present 
while True:
    if os.path.isfile(file_main):
        if os.path.isfile(file_hook_on):
            # If there is not a call already in process.
            if not os.path.isfile(file_call_on):
                print('Playing dial tone')
                dial_tone = True
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
            # If a number is being dialed and the dial tone is on, then kill the dial tone.
            if os.path.isfile(file_number):
                print('A number is being dialed. Dial tone stopped.')
                if dial_tone == True:
                    dial_tone = False
                    os.system('killall -9 vlc')
            # If a number is completed being dialed, then find the appropriate audio file to play. 
            if os.path.isfile(file_dialed):
                time.sleep(2)
                if call_in_progress == False:
                    call_in_progress = True
                    print('A number is completed being dialed. Searching for an appropriate skit or audio file.')
                    # Read in the number that was dialed.
                    num_dialed = 'wrong-number'
                    with open(file_number, 'r') as f:
                        num_dialed = f.readline().strip()
                    # Determine which file matches the numbers that were dialed.
                    # Construct the search pattern based on the num_dialed
                    pattern = "^" + num_dialed + "[_.]"

                    # Search for files in the directory that match the pattern
                    matching_files = 'wrong-number.m4a'
                    matching_files = [filename for filename in os.listdir(dir_audio) if re.search(pattern, filename)]
                    
                    # Dial the matching number and play the audio file.
                    with open(file_temp, "w") as job_file:
                        job_file.write("#!/usr/bin/python3\n")
                        job_file.write("import os\n")
                        #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
                        file = dir_audio + '/' + matching_files[0]
                        job_file.write("os.system('cvlc --no-xlib --aout=alsa " + file + "')")
                    
                    # Indicate to the player script that it should begin playing the program.
                    with open(file_player_on, "w") as job_file: # xhost + local: # to give the permissions
                        job_file.write(str(datetime.now()))
                    
                    # Print the list of matching files
                    print("Matching files:")
                    for filename in matching_files:
                        print(os.path.join(dir_audio, filename))
        else:
            # If the phone is recently placed on the hook, then stop all recordings
            if os.path.isfile(file_hook_off):
                call_in_progress = False
                # Get the time of the last modification of the file
                file_time = os.path.getmtime(file_hook_off)
                # Get the current time
                current_time = time.time()
                # Check if the file was modified in the last 5 seconds
                if current_time - file_time < 1:
                    print(f"The file {file_hook_off} was written to in the last 5 seconds.")
                    os.system('killall -9 vlc')
                    os.remove(file_call_on) if os.path.exists(file_call_on) else None
                # else:
                    # print(f"The file {file_hook_off} was not written to in the last 5 seconds.")
            else:
                print(f"The file {file_hook_off} does not exist.")
        time.sleep(0.2)
            
    else:
        time.sleep(0.2)

