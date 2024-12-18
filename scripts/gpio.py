import RPi.GPIO as GPIO
import time

class GPIOHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(4, GPIO.IN)

    def set_gpio_26(self, value: bool):
        if value:
            GPIO.output(26, GPIO.HIGH)  # Set GPIO 26 HIGH
        else:
            GPIO.output(26, GPIO.LOW)   # Set GPIO 26 LOW
        print(f"GPIO 26 set to {value}")
    
    def read_gpio(self, gpio_number):
        return GPIO.input(gpio_number)

    def cleanup(self):
        """Clean up GPIO settings before exiting."""
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    gpio_handler = GPIOHandler()
    gpio_handler.set_gpio_26(True)  # Set GPIO 26 HIGH
    print(gpio_handler.read_gpio(4))

    # Add your logic here
    time.sleep(0.5)

    gpio_handler.set_gpio_26(False)  # Set GPIO 26 LOW
    gpio_handler.cleanup()  # Clean up the GPIO setup
