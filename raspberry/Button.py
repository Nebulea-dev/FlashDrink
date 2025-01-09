import RPi.GPIO as GPIO

class FD_Button:

    BUTTON_CHANNEL = 14

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FD_Button.BUTTON_CHANNEL, GPIO.IN, GPIO.PUD_DOWN)

    @staticmethod
    def cleanup():
        GPIO.cleanup()

    @staticmethod
    def button_pressed():
        return GPIO.input(FD_Button.BUTTON_CHANNEL)


