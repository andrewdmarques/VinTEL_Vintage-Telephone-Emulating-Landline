import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)

toggle_pin = 6
led_pins = [17, 27, 22, 10, 9, 11]

GPIO.setup(toggle_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Turn on and off all LEDs based on toggle switch state
while True:
    if GPIO.input(toggle_pin) == GPIO.HIGH:
        for led in led_pins:
            GPIO.output(led, GPIO.HIGH)
    else:
        for led in led_pins:
            GPIO.output(led, GPIO.LOW)
    time.sleep(0.1)

# Clean up the GPIO pins
GPIO.cleanup()
