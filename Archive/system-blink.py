#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# system-blink.py (v1.02) indicates thet system status of the device. It
# reads from a configuration file, sets up a GPIO pin, and continuously
# checks for the presence of a file. If the file is present, it turns on
# an LED. If the file is not present, it blinks the LED twice per second.
##########################################################################
# Load libraries
##########################################################################

import os
import csv
import time
import RPi.GPIO as GPIO

##########################################################################
# User input variables
##########################################################################

# Open the configuration file and read the data
config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['description'] == 'system status':
            system_led_pin = int(row['pin'])
        elif row['variable'] == 'dir_status':
            system_working_file = row['directory'] + '/system-working.txt'
            main_on_file = row['directory'] + '/main-on.txt'

##########################################################################
# Run
##########################################################################

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(system_led_pin, GPIO.OUT)

# Define function to check for file
def check_file(file_path):
    return os.path.exists(file_path)

# Delete system-working.txt if it exists
if check_file(system_working_file):
    os.remove(system_working_file)
    
# Continuously check if system-working.txt is present
while True:
    # Check if main-on.txt is present
    if check_file(main_on_file):
        if check_file(system_working_file):
            # If the file is present, turn on the LED, counterintuitively, LOW is on.
            GPIO.output(system_led_pin, GPIO.LOW)
    else:
        GPIO.output(system_led_pin, GPIO.HIGH)
    if not check_file(system_working_file):
        # If the file is not present, blink the LED twice per second
        GPIO.output(system_led_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(system_led_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(system_led_pin, GPIO.LOW)
        time.sleep(0.01)
            
    # Wait for 1 second before checking again
    time.sleep(1)


