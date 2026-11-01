import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        GPIO.output(18, GPIO.HIGH)
        print("ON")
        time.sleep(2)

        GPIO.output(18, GPIO.LOW)
        print("OFF")
        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()