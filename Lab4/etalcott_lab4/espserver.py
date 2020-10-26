from machine import Timer, Pin
from time import sleep
import network
import ubinascii
import esp32
import socket


temp = 0
hall = 0
red_led_state = "OFF"
green_led_state = "OFF"
HOST = "192.168.137.151"
PORT = 80


# Initialize pins for LEDs
red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)


# Measure temperature, hall, and LED values
def measure_stuff():
    global temp, hall, red_led_state, green_led_state, red_led, green_led
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    red_state = red_led.value()
    if red_state == 1:
        red_led_state = "ON"
    else:
        red_led_state = "OFF"
    green_state = green_led.value()
    if green_state == 1:
        green_led_state = "ON"
    else:
        green_led_state = "OFF"
    

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    TEMP, HALL, RED_LED_STATE, GREEN_LED_STAT
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage


# Connect to the Internet
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


# Initialize and run HTTP server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)
while(1):
    # Accept a connection
    conn, addr = sock.accept()
    print('Got a connection from %s' % str(addr))
    # Check if an LED state should be updated
    data = str(conn.recv(1024))
    if data.find("/?red_led=on") == 6:
        red_led.on()
    elif data.find("/?red_led=off") == 6:
        red_led.off()
    elif data.find("/?green_led=on") == 6:
        green_led.on()
    elif data.find("/?green_led=off") == 6:
        green_led.off()
    # Create a new webpage
    measure_stuff()
    page = web_page()
    # Send the webpage as an HTTP response
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(page)
    conn.close()
