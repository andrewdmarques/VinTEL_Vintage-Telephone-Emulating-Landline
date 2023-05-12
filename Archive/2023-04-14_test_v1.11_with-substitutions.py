import RPi.GPIO as GPIO
import csv
import time
import subprocess
import threading
import re

# Define a function to check the state of an input pin
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
                    subprocess.run(command_off.split())
                    print(f'Pin {pin} is LOW, performed command_off: {command_off}')
                else:
                    # Perform command_on
                    subprocess.run(command_on.split())
                    print(f'Pin {pin} is HIGH, performed command_on: {command_on}')
        time.sleep(0.01)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Read in configure.csv
with open('/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv', 'r') as csvfile:
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
