import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up the output pin
output_pin = 18
GPIO.setup(output_pin, GPIO.OUT)

# Turn the pin on and off in a loop
try:
    while True:
        GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(output_pin, GPIO.LOW)
        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
