import RPi.GPIO as GPIO
import time

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)

toggle_pins = [6, 13, 19, 26]
led_pins = [17, 27, 22, 10, 9, 11]

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

for pin in toggle_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

toggle_leds = {6: 17, 13: 27, 19: 22, 26: 10}

# Turn the LEDs on and off one by one
while True:
    for led in led_pins:
        if led not in toggle_leds.values():
            GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(led, GPIO.LOW)
        time.sleep(0.2)

    # Check the state of the toggle switches
    for toggle_pin in toggle_pins:
        led_pin = toggle_leds.get(toggle_pin)
        GPIO.output(led_pin, GPIO.input(toggle_pin))

    # Repeat the cycle every 2 seconds
    time.sleep(1.4)

# Clean up the GPIO pins
GPIO.cleanup()
