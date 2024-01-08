import socket
import time
import RPi.GPIO as GPIO

# Server details
server_ip = '192.168.60.1'  # Server IP address
server_port = 65000

# GPIO pin connected to LDR
LDR_PIN = 18
LED_PIN = 23  # GPIO pin connected to LED

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Server details
server_ip = '192.168.60.1'  # Replace with the server's IP address
server_port = 65000
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Read light intensity
    light_intensity = GPIO.input(LDR_PIN)

    # Prepare data to send to the server
    data = {'intensity': light_intensity}
    # Send data to the server
    client_socket.send(str(data).encode())

    # Receive action from the server
    action = client_socket.recv(1024).decode()
    print("Received action from the server:", action)

    # Check the action received from the server
    if action == 'led_on':
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
        time.slee(10)
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off the LED

    # Wait for 15 seconds
    time.sleep(15)
