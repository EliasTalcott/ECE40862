from machine import Timer, Pin
from time import sleep
import network
import ubinascii
import esp32
import socket


num_reads = 0


# Connect to WebSocket
def connect_to_socket():
    addr = socket.getaddrinfo("api.thingspeak.com", 80)[0][-1]
    sock = socket.socket()
    sock.connect(addr)
    return sock
    

# Poll temperature and Hall sensors and post to ThingSpeak
def poll_sensors(p):
    global num_reads
    if num_reads < 30:
        num_reads += 1
        # Read sensors
        temp = esp32.raw_temperature()
        hall = esp32.hall_sensor()
        # Print sensor values
        print("Read number: {}  Temperature: {}  Hall: {}".format(num_reads, temp, hall))
        # Write temperature value to ThingSpeak
        addr = socket.getaddrinfo("api.thingspeak.com", 80)[0][-1]
        sock = socket.socket()
        sock.connect(addr)
        # Switch back and forth due to request limit
        sock.send(b"GET /update?api_key=UR97U0671DKS6V94&field1={}&field2={} HTTP/1.0\r\n\r\n".format(temp, hall))
        sleep(0.1)
        sock.close()
        

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


# Setup a 15s timer for sensor polling
tim_sleep = Timer(0)
tim_sleep.init(period=16000, mode=Timer.PERIODIC, callback=poll_sensors)
