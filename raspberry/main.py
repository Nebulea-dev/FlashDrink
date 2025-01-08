from enum import Enum
from time import sleep

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

    UID = read_tag()
    if UID is not None:
        customer_tag_UID = UID
        current_state = States.IDENTIFYING_TAG


def handle_identifying_tag():
    global current_state
    global customer_tag_UID
    global customer_balance

    UID = get_id_of_tag(customer_tag_UID)
    if UID is not None:
        customer_UID = UID
        customer_balance = get_balance(customer_UID)
        current_state = States.IDLE
    else:
        current_state = States.ERROR


def handle_idle():
    global current_state
    global customer_tag_UID

    # If tag is still present
    if read_tag() != customer_tag_UID:
        current_state = States.INIT
        return

    if button_pressed():
        current_state = States.PUMPING
        return


def handle_pumping():
    global current_state
    global customer_tag_UID
    global customer_balance

    # If tag is still present
    if read_tag() != customer_tag_UID:
        stop_pump()
        current_state = States.INIT
        return

    if not button_pressed():
        stop_pump()
        current_state = States.IDLE
        return

    if customer_balance == 0:
        stop_pump()
        current_state = States.INSUFFISANT_BALANCE
        return

    start_pump()
    customer_balance -= 0.01
    customer_balance = round(customer_balance, 2)
    customer_balance = max(customer_balance, 0)

    display_letters(str(customer_balance))

    sleep(0.1)


def handle_insuffisant_balance():
    global current_state
    global customer_tag_UID
    global customer_UID
    global customer_balance

    # If tag is still present
    if read_tag() != customer_tag_UID:
        current_state = States.INIT
        return

    balance = get_balance(customer_UID)
    if balance != 0:
        customer_balance = balance
        current_state = States.IDLE
        return
    
def handle_error():
    global current_state

    # If tag is still present
    if read_tag() != customer_tag_UID:
        current_state = States.INIT
        return

    display_letters("Err ")

while True:
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

    print("Unknown state")

