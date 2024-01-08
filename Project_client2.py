import RPi.GPIO as GPIO
import Adafruit_DHT
import socket
import time

# Set up DHT11 sensor
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin number where the sensor is connected

# Set up buzzer GPIO pin
buzzer_pin = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Server details
server_ip = '192.0168.60.1'  # Replace with the server's IP address
server_port = 5000

def read_temperature():
    # Read temperature from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return temperature

# Establish socket connection with the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    # Read the temperature
    temperature = read_temperature()
    print('Temperature:', temperature)

    # Send temperature data to the server
    client_socket.sendall(str(temperature).encode())

    # Receive action from the server
    action = client_socket.recv(1024).decode()
    print('Received action from the server:', action)

    # Process the action and perform necessary operations
    if action == 'Buzzer On':
        # Turn on the buzzer
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(10)
        GPIO.output(buzzer_pin, GPIO.LOW)
        
    else:
        # Turn off the buzzer
        GPIO.output(buzzer_pin, GPIO.LOW)

    # Wait for 30 seconds before reading the temperature again
    time.sleep(30)

# Close the connection
client_socket.close()
