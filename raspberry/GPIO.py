import RPi.GPIO as GPIO
from collections import deque

import sys
import signal

BUTTON_CHANNEL = 14
MAXLEN = 500

latest_inputs = deque(maxlen=MAXLEN)

def signal_handler(sig, frame):
    print("Exiting gracefully")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_CHANNEL, GPIO.IN)

old_flag = True
while True:
    latest_inputs.append(GPIO.input(BUTTON_CHANNEL))
    flag = True
    for input in latest_inputs:
        flag = flag and input

    if old_flag != flag:
        print(flag)

    old_flag = flag
