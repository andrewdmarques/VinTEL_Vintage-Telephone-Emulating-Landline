#!/usr/bin/python

import os
import time
import RPi.GPIO as GPIO

##########################################################################
# User input variables
##########################################################################
system_led_pin = 17
system_working_file = '/home/pi/Desktop/VinTEL/Bin/Status/system-working.txt'
main_on_file = '/home/pi/Desktop/VinTEL/Bin/Status/main-on.txt'

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
    if not check_file(main_on_file):
        GPIO.output(system_led_pin, GPIO.LOW)
    else:
        if check_file(system_working_file):
            # If the file is present, turn off the LED
            GPIO.output(system_led_pin, GPIO.HIGH)
        else:
            # If the file is not present, blink the LED twice per second
            GPIO.output(system_led_pin, GPIO.LOW)
            time.sleep(0.01)
            GPIO.output(system_led_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(system_led_pin, GPIO.LOW)
            time.sleep(0.01)


        
    # Wait for 1 second before checking again
    time.sleep(1)
