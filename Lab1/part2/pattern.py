from machine import Pin
from time import sleep


# Initialize inputs, outputs and states
switch_1 = Pin(32, Pin.IN)
switch_2 = Pin(33, Pin.IN)
led_green = Pin(14, Pin.OUT)
led_red = Pin(15, Pin.OUT)
switch_1_state = switch_1.value()
switch_2_state = switch_2.value()


# Allow 10 inputs from either switch before going to alternating pattern
presses_1 = 0
presses_2 = 0
while presses_1 < 20 and presses_2 < 20:
    # Check for state changes
    if switch_1.value() != switch_1_state:
        switch_1_state = switch_1.value()
        presses_1 += 1
        # If both switches ON or OFF, both LEDs OFF
        if (switch_1.value() == 0 and switch_2.value() == 0) or (switch_1.value() == 1 and switch_2.value() == 1):
            led_green.value(0)
            led_red.value(0)
        # If switches mismatched, red LED should match with switch 1 and green LED should match with switch 2
        else:
            led_green.value(switch_2.value())
            led_red.value(switch_1.value())
    if switch_2.value() != switch_2_state:
        switch_2_state = switch_2.value()
        presses_2 += 1
        # If both switches ON or OFF, both LEDs OFF
        if (switch_1.value() == 0 and switch_2.value() == 0) or (switch_1.value() == 1 and switch_2.value() == 1):
            led_green.value(0)
            led_red.value(0)
        # If switches mismatched, red LED should match with switch 1 and green LED should match with switch 2
        else:
            led_green.value(switch_2.value())
            led_red.value(switch_1.value())
    sleep(0.1)
    
    
# Determine which switch triggered end condition
if presses_1 > presses_2:
    trigger = switch_2
else:
    trigger = switch_1
trigger_state = trigger.value()


# Infinitely loop alternating pattern
led_green.value(0)
led_red.value(1)
while trigger.value() == trigger_state:
    led_green.value(not led_green.value())
    led_red.value(not led_red.value())
    sleep(0.2)


# Turn off both LEDs and exit program
led_green.value(0)
led_red.value(0)
print("You have successfully implemented LAB1 DEMO!!!")
