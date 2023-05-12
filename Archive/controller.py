#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# controller.py (v1.04) determines what "status" the device is in based on
# the control box setting. Depending on the switches that are flicked, it
# will generate the status text files to communicate to the other scripts
# what the status is. It will also control some of the LED lights.
##########################################################################
# Load libraries
##########################################################################

import RPi.GPIO as GPIO
import csv
import time
from datetime import datetime
import subprocess
import threading
import re
import os

##########################################################################
# User input variables
##########################################################################

file_config = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

##########################################################################
# Initialize
##########################################################################

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
dir_dial   = '/home/pi/Desktop/VinTEL/Bin/Status/Dial'
with open(file_config) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']
            dir_dial = dir_status + '/Dial'

##########################################################################
# Define functions
##########################################################################

# Function that updates the configuration file to have the correct directories in the commands.
def update_config_file(csv_file_path):
    # Create an empty dictionary to store the mapping between variables and directories
    directory_mapping = {}

    # Open the CSV file and read its contents
    try:
        with open(csv_file_path, 'r') as csvfile:
            config_reader = csv.DictReader(csvfile)

            # Loop through each row in the CSV file
            for row in config_reader:
                # Store the mapping between the variable and the directory
                directory_mapping[row['variable']] = row['directory']
    except Exception as e:
        print("Error reading CSV file: " + str(e))
        return

    # Update the command_on and command_off columns
    updated_rows = []
    with open(csv_file_path, 'r') as csvfile:
        config_reader = csv.DictReader(csvfile)

        # Loop through each row in the CSV file
        for row in config_reader:
            # Update the command_on and command_off columns
            updated_row = {}
            for key, value in row.items():
                if key == 'command_on' or key == 'command_off':
                    # Replace the variable substring with the corresponding directory
                    for var, dir in directory_mapping.items():
                        value = value.replace(var, dir)
                updated_row[key] = value

            # Add the updated row to the list
            updated_rows.append(updated_row)

    # Save the updated config file
    output_file_path = os.path.join(os.path.dirname(csv_file_path), 'configure_temp.csv')
    try:
        with open(output_file_path, 'w', newline='') as csvfile:
            fieldnames = updated_rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
    except Exception as e:
        print("Error writing CSV file: " + str(e))
        return
    
# Function to check the state of an input pin.
def check_input_pin(pin, command_on, command_off, variable_map):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    last_state = GPIO.input(pin)

    while True:
        state = GPIO.input(pin)

        if state != last_state:
            time.sleep(0.01)
            state = GPIO.input(pin)
            if state != last_state:
                last_state = state
                if state == GPIO.LOW:
                    # Perform command_off
                    # subprocess.run(command_off.split())
                    os.system(command_off)
                    print(f'Pin {pin} is LOW, performed command_off: {command_off}')
                else:
                    # Perform command_on
                    #subprocess.run(command_on.split())
                    os.system(command_on)
                    print(f'Pin {pin} is HIGH, performed command_on: {command_on}')
        time.sleep(0.01)

##########################################################################
# Initialize
##########################################################################

# Sleep to allow edits to be made before device powers on.
print('Initialization Complete. Entering waiting period...')
time.sleep(30)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Correct the configuration file.
update_config_file(file_config)
file_config_temp = os.path.dirname(file_config) + '/configure_temp.csv'

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['variable'] == 'dir_status':
            dir_status = row['directory']
            
system_working_file = dir_status + '/system-working.txt'
dir_dial            = dir_status + '/Dial'

# Make directories if they do not already exist. 
if not os.path.exists(dir_dial):
    os.makedirs(dir_dial)

# Indicate that initialization is complete.
with open(system_working_file, "w") as job_file: # xhost + local: # to give the permissions
    job_file.write(str(datetime.now()))
    
##########################################################################
# Run
##########################################################################

print('Beginning script..')

# Read in configure.csv
with open(file_config_temp, 'r') as csvfile:
    config_reader = csv.DictReader(csvfile)
    variable_map = {}  # Dictionary to map variables to directory paths
    threads = []
    for row in config_reader:
        if not row['pin']:
            print(f'Missing value in "pin" column for row {config_reader.line_num}')
            continue

        try:
            pin = int(row['pin'])
        except ValueError:
            print(f'Invalid value in "pin" column for row {config_reader.line_num}')
            continue

        gpio_type = row['type']
        command_on = row['command_on']
        command_off = row['command_off']

        # Iterate over the variable_map dictionary and perform variable substitution on command_on and command_off strings
        if variable_map:
            for variable, directory in variable_map.items():
                command_on = re.sub(variable, directory, command_on)
                command_off = re.sub(variable, directory, command_off)

        # If both the 'variable' and 'directory' values are not empty, replace the variable in the command_on and command_off strings with the corresponding directory path
        variable = row['variable']
        directory = row['directory']
        if variable and directory:
            command_on = command_on.replace(variable, directory)
            command_off = command_off.replace(variable, directory)
            variable_map[variable] = directory

        if gpio_type == 'in':
            # Create a thread for this input pin check
            t = threading.Thread(target=check_input_pin, args=(pin, command_on, command_off, variable_map))
            threads.append(t)
            t.start()

    # Wait for all threads to finish before exiting
    for t in threads:
        t.join()



