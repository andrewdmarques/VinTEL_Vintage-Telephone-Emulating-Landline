#!/usr/bin/python
##########################################################################
# Description
##########################################################################
# coins.py (v1.02) determines what coins were placed into the phone. After
# controller.py makes the files, then this script renames the files to have
# a time stamp added to the file name, and detects if the 25 cent and 10
# cent sensors went off, then this should just be a 10 cent. 
##########################################################################
# Load libraries
##########################################################################

import os
import csv
import time
from datetime import datetime

##########################################################################
# Functions
##########################################################################

# Function that updates the lifetime coin count.
def increment_file_count(dir_path, increment):
    found_file = False
    for filename in os.listdir(dir_path):
        if filename.startswith('deposited-lifetime-total-') and filename.endswith('.txt'):
            count_str = filename.split('-')[-1][:-4] # extract the count value from the filename
            try:
                count = int(count_str) # convert the count value to an integer
                new_count = count + increment # increment the count value
                new_filename = 'deposited-lifetime-total-{}.txt'.format(new_count) # create the new filename
                os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename)) # rename the file
                print("File '{}' renamed to '{}'".format(filename, new_filename))
                found_file = True
            except ValueError:
                print("Invalid count value in filename '{}': {}".format(filename, count_str))
    if not found_file:
        new_filename = 'deposited-lifetime-total-{}.txt'.format(increment)
        with open(os.path.join(dir_path, new_filename), 'w') as f:
            print("Created new file '{}'".format(new_filename))

##########################################################################
# Initialize
##########################################################################

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status/'
config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']

# Upon initial bootup, clear all the previous records of coin collections.
try:
    os.system('rm -r ' + dir_status + '/detected*')
except:
    pass
try:
    os.system('rm -r ' + dir_status + '/deposited-daily*')
except:
    pass
    
file_5  = dir_status + '/detected-5-cent.txt'
file_10 = dir_status + '/detected-10-cent.txt'
file_25 = dir_status + '/detected-25-cent.txt'

##########################################################################
# Run
##########################################################################
print('running coins.py...')

tot = 0
tot_prev = 0

while True:
    if os.path.exists(file_5):
        os.rename(file_5, file_5[:-4] + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
        tot += 5
    if os.path.exists(file_10):
        file_10_time = os.path.getctime(file_10)
        os.rename(file_10, file_10[:-4] + '_' + datetime.fromtimestamp(file_10_time).strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
        time.sleep(0.75)
        if os.path.exists(file_25):
            file_25_time = os.path.getctime(file_25)
            if (file_10_time - file_25_time) < 0.75:
                os.remove(file_25)
        tot += 10
    if os.path.exists(file_25):
        os.rename(file_25, file_25[:-4] + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt')
        tot += 25
    if tot != tot_prev: # If there is a new deposit, then update the deposit total file.
        # Update the daily total deposits.
        try:
            os.system('rm -r ' + dir_status + '/deposited-daily-' + str(tot_prev) + '.txt')
        except:
            pass
        with open(dir_status + '/deposited-daily-' + str(tot) + '.txt', 'w') as f:
            pass
        
        # Update the lifetime total deposits.
        increment = tot - tot_prev
        increment_file_count(dir_status, increment)

        tot_prev = tot
        
    time.sleep(0.1)





