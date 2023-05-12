import RPi.GPIO as GPIO

# Set the pin numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Set up the input and output pins
GPIO.setup(12, GPIO.IN)
GPIO.setup(9, GPIO.OUT)

# Continuously check the state of the button and update the LED
while True:
    if GPIO.input(12) == GPIO.HIGH:
        GPIO.output(9, GPIO.HIGH)
    else:
        GPIO.output(9, GPIO.LOW)
