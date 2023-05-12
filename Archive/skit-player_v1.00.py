#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# skit-player.py (v1.00) when activated that a skit should be initiated,
# this script follows the skit csv instructions to initiate the skit.
##########################################################################
# Load libraries
##########################################################################

import time
from datetime import datetime
import csv
import os
import re
import random               # For selecting a random file to play from.
#import pandas as pd         # For opening the skit file to be read.
# from mutagen.mp3 import MP3 # For determining the length of the mp3 file.


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

file_main     = dir_status + '/main-on.txt'       # The file that indicates the main switch is toggled to the on position.
file_hook_on  = dir_status + '/hook-on.txt'       # The file that indicates the handset was picked up, the hook is toggled to the on position.
file_hook_off = dir_status + '/hook-off.txt'      # The file that indicates the handset was placed down, the hook is toggled to the off position.
file_call_on  = dir_status + '/call-on.txt'       # The file that indicates there is already a call in progress.
file_dialed   = dir_status + '/dial-complete.txt' # The file that indicates that a number is completed being dialed.
file_number   = dir_status + '/Dial/number.txt'   # The file containing the dialed numbers on the first line.
file_skit_on  = dir_status + '/skit-on.txt'       # The file that indicates that a skit should be played, beginning skit-player.py.
file_player_on = dir_scripts + '/player-on.txt'   # The file that indicates that that vlc should be activated and begin playing the selected audio file.
file_temp      = dir_scripts + '/temp.py'         # The file that contains the commands to play the specified audio file.
file_skit_wait = dir_status + '/skit-wait.txt'    # The file that indicates that a skit should waint until action is performed.
action         = 'unknown'                        # This must be reset between file types, it is used to trigger search for input type (dial, hook, audio, coin).

# Make sure the skit knows to move on regardless of the condition from the last skit status.
if os.path.isfile(file_skit_wait):
    os.system('rm -r ' + file_skit_wait)
##########################################################################
# Run
##########################################################################
print('Running...')

# Main on and the skit file must be present 
while True:
    if os.path.isfile(file_main):
        if os.path.isfile(file_skit_on):
            time.sleep(0.1) # Pause to make sure the file has enough time to be written.
            # Determine which skit file should be played, retrieve this from file_skit_on.
            with open(file_skit_on, 'r') as file:
                file_skit = dir_audio + '/' + file.readline().strip()
            
            # Remove the file once the data has been extracted.
            if os.path.isfile(file_skit_on):
                os.system('rm -r ' + file_skit_on)

            # Determine all the data in the skit csv file.
            current_file = []
            first_file = []
            input_type = []
            input_value = []
            next_file = []

            with open(file_skit, 'r') as file:
                reader = csv.reader(file)
                next(reader) # skip header row
                for row in reader:
                    current_file.append(row[0])
                    first_file.append(row[1])
                    input_type.append(row[2])
                    input_value.append(row[3])
                    next_file.append(row[4])
                    
            # Determine what the starting point is.
            # Loop through first_file column and assign corresponding current_file to file_active
            for i in range(len(first_file)):
                if first_file[i] == 'yes':
                    file_active = current_file[i]
                    break # Stop looping once first "yes" response is found
            
            # Remove the skit wait file if it is present.
            if os.path.isfile(file_skit_wait):
                os.system('rm -r ' + file_skit_wait)
            
            # Begin loop that determines which skit should be played and if the skit is done running.
            complete = False
            while complete == False:
                if not os.path.isfile(file_skit_wait):
                    
                    # Make the skit wait until the actions are done.
                    with open(file_skit_wait, "w") as job_file: # xhost + local: # to give the permissions
                        job_file.write(str(datetime.now()))
                    action == 'unknown'
                    
                    print(file_active)
                    # check if current_file is an mp3 file
                    if os.path.splitext(file_active)[1] in ('.mp3','.wav', '.m4a'):
                        os.system('killall -9 vlc')
                        print('playing ' + file_active)
                        # Initiate the audio file to begin being played.
                        with open(file_temp, "w") as job_file:
                            job_file.write("#!/usr/bin/python3\n")
                            job_file.write("import os\n")
                            #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
                            file = dir_audio + '/' + file_active
                            job_file.write("os.system('cvlc --no-xlib --aout=alsa " + file + "')\n")
                            job_file.write("os.system('rm -r " + file_skit_wait + "')")
                        # Indicate to the player script that it should begin playing the program.
                        with open(file_player_on, "w") as job_file: # xhost + local: # to give the permissions
                            job_file.write(str(datetime.now()))
                        time.sleep(4)
                            
                    # Check if the current file is a python script, then make it appropriately.
                    if os.path.splitext(file_active)[1] in ('.py'):
                        # Initiate the audio file to begin being played.
                        with open(file_temp, "w") as job_file:
                            job_file.write("#!/usr/bin/python3\n")
                            job_file.write("import os\n")
                            #job_file.write("media = '"+prog_dir_curr[0]+"'\n")
                            file = dir_audio + '/' + file_active
                            job_file.write("os.system('chmod +x " + file + "')\n")
                            job_file.write("os.system('python3 " + file + "')\n")
                            job_file.write("os.system('rm -r " + file_skit_wait + "')\n")
                        # Indicate to the player script that it should begin playing the program.
                        with open(file_player_on, "w") as job_file: # xhost + local: # to give the permissions
                            job_file.write(str(datetime.now()))
                        
                # If necessary actions are NOT met for the skit to move on, then wait until they are to continue.
                if os.path.isfile(file_skit_wait):
                    print('skit_waiting for response')
                    
                    # Determine what type of action must be met.
                    if action == 'unknown':
                        for ii in range(0,len(current_file)):
                            if current_file[ii] == file_active:
                                action = input_type[ii]
                    
                    # If hook on is the action item.
                    if action == 'hook':
                        # Determine what the next current file should be.
                        for ii in range(0,len(current_file)):
                            if current_file[ii] == file_active:
                                if os.path.isfile(file_hook_on):
                                    # Tell the skit file to move on.
                                    os.system('rm -r ' + file_skit_wait)
                                    os.system('killall -9 vlc')
                                    # Update the active file to move on to the next item in the list.
                                    file_active = next_file[ii]
                    
                    # If number must be dialed.
                    if action == 'dial':
                        print('Searching for dial response')
                        # Check if the file exists
                        if os.path.exists(file_number):
                            print('number.txt exists')
                            # Get the modification time of the file
                            mtime = os.path.getmtime(file_number)
                            # Check if the file was modified more than 3 seconds ago
                            if time.time() - mtime > 2:
                                os.system('rm -r ' + file_skit_wait)
                                os.system('killall -9 vlc')
                                # Read the contents of the file and save them in number_dialed
                                number_dialed = 1234567890
                                with open(file_number, "r") as f:
                                    print('number.txt being opened')
                                    # Extract the number that was dialed.
                                    number_dialed = f.read().strip()
                                print('Number dialed: ',str(number_dialed))
                                # Determine which file is associated with the number.
                                file_active1 = file_active
                                for ii in range(0,len(current_file)):
                                    if current_file[ii] == file_active:
                                        if number_dialed == input_value[ii]:
                                            file_active1 = next_file[ii]
                                            print('Number dialed and located: ' + str(number_dialed))
                                if file_active1 == file_active:
                                    file_active = 'wrong-number.m4a'
                                else:
                                    file_active = file_active1
                    # If audio must be captured.
                    
                    # If coints must be deposited.
                    
                    
                if os.path.isfile(file_hook_off):
                    complete = True
                    os.system('rm -r ' + dir_status + '/skit*')
                time.sleep(0.2)        
                
    time.sleep(0.2)
    
