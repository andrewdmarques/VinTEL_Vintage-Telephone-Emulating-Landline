import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up the input and output pins
input_pin = 6
output_pin = 18
GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(output_pin, GPIO.OUT)

# Set up the LED pins
led_pins = [17, 27, 22, 10, 9, 11]
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Define a function to control the relay and LEDs
def toggle_relay(channel):
    if GPIO.input(input_pin):
        GPIO.output(output_pin, GPIO.LOW)
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
    else:
        GPIO.output(output_pin, GPIO.HIGH)
        for pin in led_pins:
            GPIO.output(pin, GPIO.HIGH)

# Add an event listener to the input pin
GPIO.add_event_detect(input_pin, GPIO.BOTH, callback=toggle_relay)

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
