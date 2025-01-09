import RPi.GPIO as GPIO

class FD_Pump:
    PUMP_CHANNEL = 15

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FD_Pump.PUMP_CHANNEL, GPIO.OUT)

    @staticmethod
    def start_pump():
        GPIO.output(FD_Pump.PUMP_CHANNEL, GPIO.HIGH)

    @staticmethod
    def stop_pump():
        GPIO.output(FD_Pump.PUMP_CHANNEL, GPIO.LOW)
    
    @staticmethod
    def cleanup():
        GPIO.cleanup()
