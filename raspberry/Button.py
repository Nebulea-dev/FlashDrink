import RPi.GPIO as GPIO
from collections import deque

class FD_Button:

    BUTTON_CHANNEL = 14
    MAXLEN = 500

    latest_inputs = deque(maxlen=MAXLEN)

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FD_Button.BUTTON_CHANNEL, GPIO.IN)

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    @staticmethod
    def update_button_state():
        FD_Button.latest_inputs.append(GPIO.input(FD_Button.BUTTON_CHANNEL))

    @staticmethod
    def button_pressed():
        flag = True
        for input in FD_Button.latest_inputs:
            flag = flag and input

        return flag


