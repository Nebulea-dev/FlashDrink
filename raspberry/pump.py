import RPi.GPIO as GPIO

import sys
import signal

PUMP_CHANNEL = 21

def signal_handler(sig, frame):
    print("Exiting gracefully")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUMP_CHANNEL, GPIO.OUT)



while True:
    print(GPIO.input(PUMP_CHANNEL))
    GPIO.output(PUMP_CHANNEL, GPIO.HIGH)
