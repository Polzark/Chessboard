import time
import RPi.GPIO as GPIO

LOAD_PIN = 17
CLOCK_PIN = 27
DATA_PIN = 24

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
    while True:
        readings = read_shift_register()
        print(readings)
        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()