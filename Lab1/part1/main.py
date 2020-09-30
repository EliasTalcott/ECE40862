import time
from machine import Pin


def flash_led():
    led = Pin(13, Pin.OUT)
    enable = True
    while True:
        led.value(enable)
        enable = not enable
        time.sleep(1)


if __name__ == "__main__":
    flash_led()