#!/usr/bin/env python3

from machine import Pin, I2C, PWM, Timer
from time import sleep
import MPU

# Initialize GPIO
switch_1 = Pin(33, Pin.IN)
switch_2 = Pin(27, Pin.IN)
active_switch = switch_1
red_led = Pin(14, Pin.OUT)
yellow_led = Pin(32, Pin.OUT)
green_led = Pin(15, Pin.OUT)
onboard_led = Pin(13, Pin.OUT)
demo = False

# Initialize I2C and declare sensors
i2c = I2C(scl=Pin(22), sda=Pin(23))
myMpu = None
temp_timer = Timer(0)

# Initialize temperature variables
temp_init = None
temp_change = None
led_on = False

# Initialize speed variables
speed_x = 0
speed_y = 0
speed_z = 0
speed_timer = Timer(1)

# Debounce switch presses
def debounce(pin):
    # Make sure switch is pressed for 10ms
    count = 0
    while count < 5:
        if pin.value() == 1:
            count += 1
            sleep(0.001)
        else:
            return
    # Call function based on switch pressed
    if pin == switch_1:
        init_sensors()
        return
    elif pin == switch_2:
        run_spinner()
        return
    else:
        raise Exception("Pin {} is not a valid switch".format(pin))


# Initialize sensors
def init_sensors():
    global myMpu, onboard_led, active_switch, led_on, demo
    demo = False
    temp_timer.init(period=1000, mode=Timer.PERIODIC, callback=set_freq)
    speed_timer.init(period=100, mode=Timer.PERIODIC, callback=set_speed)
    led_on = False
    # Enable onboard LED in standard mode
    onboard_led = Pin(13, Pin.OUT)
    onboard_led.value(1)
    # Initialize MPU and wait for state change
    myMpu = MPU.MPU(i2c)
    while True:
        if switch_2.value() == 1:
            active_switch = switch_2
            return
        sleep(0.01)


# Run Spinner
def run_spinner():
    global myMpu, onboard_led, active_switch, temp_init, temp_change, led_on, demo
    demo = True
    onboard_led = PWM(Pin(13), freq=10, duty=512)
    # Initialize temperature print timer
    temp_init = myMpu.temperature()
    led_on = True
    while True:
        # Check for state change
        if switch_1.value() == 1:
            onboard_led.deinit()
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            active_switch = switch_1
            return

        # Control onboard LED based on temperature change
        temp_change = myMpu.temperature() - temp_init
        if not led_on and temp_change >= -2:
            onboard_led = PWM(Pin(13), freq=int(10 + (5 * temp_change)), duty=512)
            led_on = True
        elif led_on and temp_change < -2:
            onboard_led.deinit()
            onboard_led = Pin(13, Pin.OUT)
            onboard_led.value(0)
            led_on = False

        # Check for excessive speed
        if abs(speed_x) > 3 or abs(speed_y) > 3 or speed_z > 3:
            red_led.value(1)
        else:
            red_led.value(0)

        # Check for excessive tilt
        if abs(myMpu.pitch) > 30 or abs(myMpu.roll) > 30 or abs(myMpu.yaw) > 30:
            yellow_led.value(1)
        else:
            yellow_led.value(0)

        # Check for motionless condition (less than 1 to account for accelerometer drift)
        if abs(speed_x) < 1 and abs(speed_y) < 1 and abs(speed_z) < 1:
            green_led.value(1)
        else:
            green_led.value(0)


def set_speed(p):
    global speed_x, speed_y, speed_z
    acc_x, acc_y, acc_z = myMpu.acceleration()
    speed_x += (acc_x * 0.1) - 0.0005
    speed_y += (acc_y * 0.1) - 0.004
    speed_z += ((acc_z - 9.75) * 0.1) + 0.002


def set_freq(p):
    global cycles
    if demo:
        if led_on:
            onboard_led.freq(int(10 + (5 * temp_change)))
        cycles += 1
        # print("adPitch: {}, adRoll: {}, adYaw: {}".format(myMpu.pitch / cycles, myMpu.roll / cycles, myMpu.yaw / cycles))
        print("Pitch: {}, Roll: {}, Yaw: {}, Temperature: {}".format(myMpu.pitch, myMpu.roll, myMpu.yaw, myMpu.temperature()))
        # print("adX: {}, adY: {}, adZ: {}".format(speed_x / cycles / 10, speed_y / cycles / 10, speed_z / cycles / 10))
        # print("speed_x: {}, speed_y: {}, speed_z: {}".format(speed_x, speed_y, speed_z))

cycles = 0

# Wait for switch 1 press to initialize sensors
while True:
    if active_switch.value() == 1:
        debounce(active_switch)
