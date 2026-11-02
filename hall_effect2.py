
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


try:
    print("Reading Hall sensors... Press Ctrl+C to stop.")

    while True:
        readings = read_shift_register()

        # First register is read after the second register.
        # Therefore, readings[0:8] = sensors 9-16
        # and readings[8:16] = sensors 1-8.

        # Map each physical sensor position to its LED
        for i in range(16):
            if i < 8:
                sensor_reading = readings[15 - i]
            else:
                sensor_reading = readings[23 - i]

            if sensor_reading == PIECE_DETECTED_STATE:
                pixels[i] = (255, 0, 0)
            else:
                pixels[i] = (0, 0, 0)

        pixels.show()
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()
