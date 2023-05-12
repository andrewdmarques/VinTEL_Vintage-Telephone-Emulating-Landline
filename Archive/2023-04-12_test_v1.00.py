import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

leds = [17, 27, 22, 10, 9, 11]
state = False

# Turn the LEDs on and off one by one
while True:
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.1)

    # Repeat the cycle every 2 seconds
    time.sleep(0.4)

# Clean up the GPIO pins
GPIO.cleanup()