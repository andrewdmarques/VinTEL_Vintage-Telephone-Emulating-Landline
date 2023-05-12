import RPi.GPIO as GPIO
import csv
import time
import threading

# Define a function to check the state of an input pin
def check_input_pin(pin, command_on, command_off):
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
                    print(f'Pin {pin} is LOW, performing command_off: {command_off}')
                else:
                    # Perform command_on
                    print(f'Pin {pin} is HIGH, performing command_on: {command_on}')
        time.sleep(0.01)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Read in configure.csv
with open('/home/pi/Desktop/VinTEL/Bin/Scripts/configure.csv', 'r') as csvfile:
    config_reader = csv.DictReader(csvfile)
    threads = []
    for row in config_reader:
        if row['pin']:
            try:
                pin = int(row['pin'])
            except ValueError:
                print(f'Invalid value in "pin" column for row {config_reader.line_num}')
                continue
        else:
            print(f'Missing value in "pin" column for row {config_reader.line_num}')
            continue

        gpio_type = row['type']
        command_on = row['command_on']
        command_off = row['command_off']
        
        if gpio_type == 'in':
            # Create a thread for this input pin check
            t = threading.Thread(target=check_input_pin, args=(pin, command_on, command_off))
            threads.append(t)
            t.start()

    # Wait for all threads to finish before exiting
    for t in threads:
        t.join()
