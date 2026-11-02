
import time
import board
import neopixel
import RPi.GPIO as GPIO

# Shift register pins (BCM)
LOAD_PIN = 17
CLOCK_PIN = 27
DATA_PIN = 24

PIECE_DETECTED_STATE = GPIO.LOW

# LED setup
LED_COUNT = 16
pixels = neopixel.NeoPixel(
    board.D18,
    LED_COUNT,
    brightness=0.2,
    auto_write=False
)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LOAD_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(CLOCK_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DATA_PIN, GPIO.IN)


def read_shift_register():
    bits = []

    GPIO.output(LOAD_PIN, GPIO.LOW)
    time.sleep(0.00001)
    GPIO.output(LOAD_PIN, GPIO.HIGH)

    for _ in range(16):
        bits.append(GPIO.input(DATA_PIN))

        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)

    return bits

led_mapping = [
    0, 1, 2, 3,       # Sensors 1-4
    7, 6, 5, 4,       # Sensors 5-8
    8, 9, 10, 11,     # Sensors 9-12
    15, 14, 13, 12    # Sensors 13-16
]

try:
    print("Reading Hall sensors... Press Ctrl+C to stop.")

    while True:
        readings = read_shift_register()

        # First register is read after the second register.
        # Therefore, readings[0:8] = sensors 9-16
        # and readings[8:16] = sensors 1-8.

        # Map each physical sensor position to its LED
        for i in range(16):
            sensor_index = (i + 8) % 16
            led_index = led_mapping[i]

            if readings[sensor_index] == PIECE_DETECTED_STATE:
                pixels[led_index] = (255, 0, 0)
            else:
                pixels[led_index] = (0, 0, 0)

        pixels.show()
        print(readings)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()
