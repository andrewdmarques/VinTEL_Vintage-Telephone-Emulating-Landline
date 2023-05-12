import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)

toggle_pin1 = 26
toggle_pin2 = 19

GPIO.setup(toggle_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(toggle_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main loop
while True:
    # Check toggle switch 1 state
    toggle_state1 = GPIO.input(toggle_pin1)
    if not toggle_state1:
        print("Toggle switch 1 is ON")
    else:
        print("Toggle switch 1 is OFF")

    # Check toggle switch 2 state
    toggle_state2 = GPIO.input(toggle_pin2)
    if not toggle_state2:
        print("Toggle switch 2 is ON")
    else:
        print("Toggle switch 2 is OFF")

    time.sleep(0.1)
