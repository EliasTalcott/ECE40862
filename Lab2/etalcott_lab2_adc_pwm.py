from machine import RTC, Timer, Pin, PWM, ADC
from time import sleep

switch_state = 0
control_started = False
red_control = False
adc_value = 0

# Define interrupt service routines
def print_datetime(p):
    global rtc
    global adc_value
    datetime = rtc.datetime()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    print("{}  {} {}, {}  {}:{}:{}:{}".format(weekdays[datetime[3]], months[datetime[1] - 1], datetime[2], datetime[0], datetime[4], datetime[5], datetime[6], datetime[7]))

def switch_press():
    global control_started
    global red_control
    control_started = True
    red_control = not red_control
    
def check_switch(p):
    global switch
    global switch_state
    current_state = switch.value()
    if switch_state == 0 and current_state == 1:
        switch_state = 1
        switch_press()
    elif switch_state == 1 and current_state == 0:
        switch_state = 0
    
def read_adc(p):
    global adc_value
    global pot
    adc_value = pot.read()

# Get date/time inputs as integers
while(1):
    try:
        year = input("Year? ")
        year = int(year)
        break
    except ValueError:
        print("Cannot convert year '{}' to an integer".format(year))
while(1):
    try:
        month = input("Month? ")
        month = int(month)
        break
    except ValueError:
        print("Cannot convert month '{}' to an integer".format(year))
while(1):
    try:
        day = input("Day? ")
        day = int(day)
        break
    except ValueError:
        print("Cannot convert day '{}' to an integer".format(day))
while(1):
    try:   
        weekday = input("Weekday? ")
        weekday = int(weekday)
        break
    except ValueError:
        print("Cannot convert weekday '{}' to an integer".format(weekday))
while(1):
    try:
        hour = input("Hour? ")
        hour = int(hour)
        break
    except ValueError:
        print("Cannot convert hour '{}' to an integer".format(hour))
while(1):
    try:
        minute = input("Minute? ")
        minute = int(minute)
        break
    except ValueError:
        print("Cannot convert minute '{}' to an integer".format(minute))
while(1):
    try:
        second = input("Second? ")
        second = int(second)
        break
    except ValueError:
        print("Cannot convert second '{}' to an integer".format(second))
while(1):
    try:
        microsecond = input("Microsecond? ")
        microsecond = int(microsecond)
        break
    except ValueError:
        print("Cannot convert microsecond '{}' to an integer".format(microsecond))
        
# Initialize real time clock and print datetime every 30 seconds
rtc = RTC()
rtc.init((year, month, day, weekday, hour, minute, second, microsecond))
tim_date = Timer(0)
tim_date.init(period=30000, mode=Timer.PERIODIC, callback=print_datetime)

# Initialize input and output pins
green_led = PWM(Pin(14))
red_led = PWM(Pin(15))
switch = Pin(32, Pin.IN, Pin.PULL_DOWN)
pot = ADC(Pin(34))

# Configure PWM and ADC settings
green_led.freq(10)
green_led.duty(256)
red_led.freq(10)
red_led.duty(256)
pot.atten(ADC.ATTN_11DB)

# Poll ADC every 100ms (value between 0-4095)
tim_adc = Timer(1)
tim_adc.init(period=100, mode=Timer.PERIODIC, callback=read_adc)

# Configure button interrupt
tim_switch = Timer(2)
tim_switch.init(period=50, mode=Timer.PERIODIC, callback=check_switch)

# Use the button press to switch between controlling the LEDs
while(1):
    if control_started:
        # Control frequency of red LED
        if red_control:
            red_led.freq(adc_value // 50)
            sleep(0.1)
        # Control duty cycle of green LED
        else:
            green_led.duty(adc_value // 4)
            sleep(0.1)