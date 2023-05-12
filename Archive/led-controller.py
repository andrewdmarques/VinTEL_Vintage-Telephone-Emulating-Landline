#!/usr/bin/python3
##########################################################################
# Description
##########################################################################
# led-controller.py (v1.00) determines the current state of the system to
# have it turn on/off the LED lights appropriately.
##########################################################################
# Load libraries
##########################################################################

import time
from datetime import datetime
import csv
import os
import re
import RPi.GPIO as GPIO

##########################################################################
# User input variables
##########################################################################

config_file = '/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv'

##########################################################################
# Initialize
##########################################################################
print('Initializing')

# Define the GPIO pins to be used (these are the default if there is an issues with the configure file. Expect them to be optentially overwritten.
# incoming_call_led = 11
# hook_led = 9
# motion_detected = 10
# cent_25_led = 17
# cent_10_led = 27
# cent_5_led = 22

# Open the configuration file and read the data
dir_status = '/home/pi/Desktop/VinTEL/Bin/Status'
with open(config_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['description'] == 'system status':
            system_led_pin = int(row['pin'])
        elif row['description'] == 'incoming call':
            incoming_call_led = int(row['pin'])
        elif row['description'] == 'hook and dial':
            hook_led = int(row['pin'])
        elif row['description'] == 'motion detected':
            motion_detected = int(row['pin'])
        elif row['description'] == '5 cent':
            cent_5_led = int(row['pin'])
        elif row['description'] == '10 cent':
            cent_10_led = int(row['pin'])
        elif row['description'] == '25 cent':
            cent_25_led = int(int(row['pin']))
        elif row['variable'] == 'dir_effects':
            dir_effects = row['directory']
        elif row['variable'] == 'dir_scripts':
            dir_scripts = row['directory']
        elif row['variable'] == 'dir_audio':
            dir_audio = row['directory']
        elif row['variable'] == 'dir_skits':
            dir_skits = row['directory']
        elif row['variable'] == 'dir_status':
            dir_status = row['directory']

file_main     = dir_status + '/main-on.txt'       # The file that indicates the main switch is toggled to the on position.
file_hook_on  = dir_status + '/hook-on.txt'       # The file that indicates the handset was picked up, the hook is toggled to the on position.
file_hook_off = dir_status + '/hook-off.txt'      # The file that indicates the handset was placed down, the hook is toggled to the off position.
file_call_on  = dir_status + '/call-on.txt'       # The file that indicates there is already a call in progress.
file_dialed   = dir_status + '/dial-complete.txt' # The file that indicates that a number is completed being dialed.
file_number   = dir_status + '/Dial/number.txt'   # The file containing the dialed numbers on the first line.
file_skit_on  = dir_status + '/skit-on.txt'       # The file that indicates that a skit should be played, beginning skit-player.py.
file_player_on = dir_scripts + '/player-on.txt'   # The file that indicates that that vlc should be activated and begin playing the selected audio file.
file_temp     = dir_scripts + '/temp.py'          # The file that contains the commands to play the specified audio file.
file_call_intitiated = dir_status + '/call-initiated.txt'
file_motion   = dir_status + '/detected-motion.txt'
file_5  = 'detected-5-cent'
file_10 = 'detected-10-cent'
file_25 = 'detected-25-cent'
dir_coin = dir_status + '/Deposited-Coins-Temp'

# Make a directory that all the dated coins will go into.
dir_coin_final = dir_status + '/Deposited-Coins'
if not os.path.exists(dir_coin_final):
    os.makedirs(dir_coin_final)

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(incoming_call_led, GPIO.OUT)
GPIO.setup(hook_led, GPIO.OUT)
GPIO.setup(motion_detected, GPIO.OUT)
GPIO.setup(cent_25_led, GPIO.OUT)
GPIO.setup(cent_10_led, GPIO.OUT)
GPIO.setup(cent_5_led, GPIO.OUT)

# Define a function to turn on a GPIO pin
def turn_on(pin):
    GPIO.output(pin, GPIO.HIGH)

# Define a function to turn off a GPIO pin
def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)

# Define a function to check for the presence of a file
def file_exists(file_path):
    return os.path.exists(file_path)

##########################################################################
# Run
##########################################################################
print('Running...')



# Define the time interval for turning off the call-initiated GPIO pin
CALL_INITIATED_OFF_INTERVAL = 15

# Define the duration for turning on the detected-motion GPIO pin
DETECTED_MOTION_DURATION = 15

call_initiated_time = time.monotonic()

# Loop indefinitely
while True:
    # Check for the presence of call-initiated.txt
    if file_exists(file_call_intitiated):
        turn_on(incoming_call_led)
        call_initiated_time = time.monotonic()
        print('Call initiated')
    else:
        if time.monotonic() - call_initiated_time > CALL_INITIATED_OFF_INTERVAL or file_exists(file_hook_on):
            turn_off(incoming_call_led)

    # Check for the presence of hook-on.txt and hook-off.txt
    if file_exists(file_hook_on):
        turn_on(hook_led)
        print('Hook on')
    elif file_exists(file_hook_off):
        turn_off(hook_led)
        print('Hook off')

    # Check for the presence of detected-motion.txt
    if file_exists(file_motion):
        turn_on(motion_detected)
        print('Motion detected')
        #time.sleep(DETECTED_MOTION_DURATION)
        turn_off(motion_detected)

    # Check for the presence of coin files
    for coin_file in os.listdir(dir_coin):
        if coin_file.startswith(file_25):
            print('25 cents deposited')
            turn_on(cent_25_led)
            os.system('mv ' + dir_coin + '/' + coin_file + ' ' + dir_coin_final + '/' + coin_file)
        elif coin_file.startswith(file_10):
            print('10 cents deposited')
            turn_on(cent_10_led)
            os.system('mv ' + dir_coin + '/' + coin_file + ' ' + dir_coin_final + '/' + coin_file)
        elif coin_file.startswith(file_5):
            print('5 cents deposited')
            turn_on(cent_5_led)
            os.system('mv ' + dir_coin + '/' + coin_file + ' ' + dir_coin_final + '/' + coin_file)

    # Wait for a short time before checking again
    time.sleep(0.1)
