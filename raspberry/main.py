from enum import Enum
from time import sleep

import sys
import signal

from Display import FD_Display
from Pump import FD_Pump
from Button import FD_Button
from API import FD_API
from RFID import FD_RFID

class States(Enum):
    INIT = 0
    IDENTIFYING_TAG = 1
    IDLE = 2
    PUMPING = 3
    INSUFFISANT_BALANCE = 4
    ERROR = 5

current_state = States.INIT
customer_tag_UID = None
customer_UID = None
customer_balance = 0


def handle_init():
    global current_state
    global customer_tag_UID

    FD_Display.write_letters("Err ")

    UID = FD_RFID.read_UID()
    if UID is not None:
        customer_tag_UID = UID
        current_state = States.IDENTIFYING_TAG


def handle_identifying_tag():
    global current_state
    global customer_tag_UID
    global customer_balance

    UID = FD_API.get_id_of_tag(customer_tag_UID)
    if UID is not None:
        customer_UID = UID
        customer_balance = FD_API.get_balance(customer_UID)
        current_state = States.IDLE
    else:
        current_state = States.ERROR


def handle_idle():
    global current_state
    global customer_tag_UID
    global customer_balance

    FD_Display.write_number(int(customer_balance*100))

    # If tag is still present
    if FD_RFID.read_UID() != customer_tag_UID:
        current_state = States.INIT
        return

    if FD_Button.button_pressed():
        current_state = States.PUMPING
        return


def handle_pumping():
    global current_state
    global customer_tag_UID
    global customer_balance

    # If tag is still present
    if FD_RFID.read_UID() != customer_tag_UID:
        FD_Pump.stop_pump()
        current_state = States.INIT
        return

    if not FD_Button.button_pressed() or customer_balance <= 0.0:
        FD_Pump.stop_pump()
        current_state = States.IDLE
        return

    FD_Pump.start_pump()
    customer_balance -= 1.00
    customer_balance = round(customer_balance, 2)
    customer_balance = max(customer_balance, 0)

    FD_Display.write_number(int(customer_balance*100))

    sleep(0.1)


def handle_insuffisant_balance():
    global current_state
    global customer_tag_UID
    global customer_UID
    global customer_balance

    # If tag is still present
    if FD_RFID.read_UID() != customer_tag_UID:
        current_state = States.INIT
        return

    balance = FD_API.get_balance(customer_UID)
    if balance != 0:
        customer_balance = balance
        current_state = States.IDLE
        return
    
def handle_error():
    global current_state

    # If tag is still present
    if FD_RFID.read_UID() != customer_tag_UID:
        current_state = States.INIT
        return

    FD_Display.write_letters("Err ")

def signal_handler(_sig, _frame):
    print("Exiting gracefully")
    FD_Pump.cleanup()
    FD_Button.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Init GPIOs
FD_Button.init()
FD_Pump.init()

while True:
    print(current_state)

    if current_state == States.INIT:
        handle_init()
        continue
    
    if current_state == States.IDENTIFYING_TAG:
        handle_identifying_tag()
        continue

    if current_state == States.IDLE:
        handle_idle()
        continue

    if current_state == States.PUMPING:
        handle_pumping()
        continue

    if current_state == States.INSUFFISANT_BALANCE:
        handle_insuffisant_balance()
        continue

    if current_state == States.ERROR:
        handle_error()
        continue

    print("Unknown state")

