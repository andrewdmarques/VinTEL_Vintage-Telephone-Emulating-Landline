import RPi.GPIO as GPIO

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)

# Define the input pins
toggle_pin = 6
led_pins = [13, 19, 26]

# Define the output pins
relay_pin = 18
led_pins_output = [17, 27, 22]

# Set up the input pins
GPIO.setup(toggle_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for led_pin in led_pins:
    GPIO.setup(led_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up the output pins
GPIO.setup(relay_pin, GPIO.OUT)
for led_pin_output in led_pins_output:
    GPIO.setup(led_pin_output, GPIO.OUT)

# Define the toggle function for the relay
def toggle_relay(channel):
    GPIO.output(relay_pin, not GPIO.input(relay_pin))

# Define the toggle function for the LEDs
def toggle_led(channel):
    led_pin_index = led_pins.index(channel)
    GPIO.output(led_pins_output[led_pin_index], not GPIO.input(led_pins_output[led_pin_index]))

# Add event detection for the toggle switch and LEDs
GPIO.add_event_detect(toggle_pin, GPIO.FALLING, callback=toggle_relay, bouncetime=300)
for led_pin in led_pins:
    GPIO.add_event_detect(led_pin, GPIO.FALLING, callback=toggle_led, bouncetime=300)

# Loop indefinitely to keep the program running
while True:
    pass

# Clean up the GPIO pins when the program exits
GPIO.cleanup()
