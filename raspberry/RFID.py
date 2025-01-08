import RPi.GPIO as GPIO
from mfrc522 import MFRC522

class FD_RFID:
    reader = MFRC522()

    @staticmethod
    def read_UID():
        reader = FD_RFID.reader
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status != reader.MI_OK:
            (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status != reader.MI_OK:
                return None
        (status, uid) = reader.MFRC522_Anticoll()
        if status != reader.MI_OK:
            return None

        return uid
