import RPi.GPIO as GPIO

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins
GPIO.setup(18, GPIO.OUT) # LED on pin 17
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button on pin 23

# Define a callback function to run when the button is pressed
def button_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        print("Button pressed on pin", channel)
        GPIO.output(18, GPIO.LOW) # Turn on the LED
    else:
        print("Button released on pin", channel)
        GPIO.output(18, GPIO.HIGH) # Turn off the LED

# Register the callback function for the button
GPIO.add_event_detect(23, GPIO.BOTH, callback=button_callback, bouncetime=300)

# Run the program indefinitely
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
