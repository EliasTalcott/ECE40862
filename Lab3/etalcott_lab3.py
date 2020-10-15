from machine import RTC, Timer, Pin, TouchPad, deepsleep, wake_reason
from time import sleep
import network
import ubinascii
import ntptime
import esp32


# Define interrupt service routines
def print_datetime(p):
    global rtc
    tm = rtc.datetime()
    print("Date: {:02d}/{:02d}/{:04d}\nTime: {:02d}:{:02d}:{:02d} HRS\n".format(tm[1], tm[2], tm[0], tm[4], tm[5], tm[6]))


def check_green(p):
    global touch_green
    global led_green
    if touch_green.read() < 400:
        led_green.value(1)
    else:
        led_green.value(0)


def go_to_sleep(p):
    print("I am awake. Going to sleep for 1 minute\n")
    deepsleep(60000)


# Print the wakeup cause
reason = wake_reason()
if reason == 3:
    print("\nWoke up due to button\n")
elif reason == 5:
    print("\nWoke up due to touchpad\n")
      
# Connect to WiFi hotspot and print network information
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print('Oh Yes! Get connected')
if not wlan.isconnected():
    wlan.connect('DESKTOP-ETALCOTT', '12345678')
    while not wlan.isconnected():
        pass
print("Connected to DESKTOP-ETALCOTT")
mac = ubinascii.hexlify(wlan.config('mac')).decode('utf-8')
print("MAC Address: {}:{}:{}:{}:{}:{}".format(mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12]))
print('IP Address: {}\n'.format(wlan.ifconfig()[0]))


# Initialize real time clock from pool.ntp.org, convert to Eastern Time, and print every 15 seconds
ntptime.settime()
rtc = RTC()
tm = rtc.datetime()
rtc.datetime((tm[0], tm[1], tm[2], tm[3], tm[4] - 4, tm[5], tm[6], tm[7]))
tim_date = Timer(0)
tim_date.init(period=15000, mode=Timer.PERIODIC, callback=print_datetime)


# Turn on red LED and control green LED using touch input
led_red = Pin(13, Pin.OUT)
led_red.value(1)
led_green = Pin(14, Pin.OUT)
touch_green = TouchPad(Pin(12))
tim_green = Timer(1)
tim_green.init(period=10, mode=Timer.PERIODIC, callback=check_green)


# Configure switch and touch wakeup sources
button_1 = Pin(32, Pin.IN)
button_2 = Pin(33, Pin.IN)
esp32.wake_on_ext1(pins=(button_1, button_2), level=esp32.WAKEUP_ANY_HIGH)
touch_wake = TouchPad(Pin(15))
touch_wake.config(400)
esp32.wake_on_touch(True)


# Go to sleep every 30 seconds
tim_sleep = Timer(2)
tim_sleep.init(period=30000, mode=Timer.PERIODIC, callback=go_to_sleep)


while(1):
    pass