import socket
import threading
import logging
import wx
from wx import EVT_BUTTON

# Configure logging
logging.basicConfig(filename='server1.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server details
server_ip = '192.168.41.1'  # Server IP address
server_port = 65000

# Function to handle client connections
def handle_client(client_socket, client_address):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()

        if data:
            logging.info(f'Received data from {client_address[0]}: {data}')

            if client_address[0] == '192.168.41.240':  # Replace with the actual IP address of client 1
                # Handle data from client 1 (intensity)
                intensity = data
                print(intensity)
                # Determine action based on intensity
                action = ""
                if intensity == "0":
                    print("There was No light")
                    action = "led_on"
                else:
                    action = "led_off"

                # Update GUI for client 1 with received data and action
                update_gui(client1_label, intensity_label1, None, None, action_label1, client_address[0], intensity, None, None, action)

                # Send action to client 1
                client_socket.sendall(action.encode())
                logging.info(f'Sent action to {client_address[0]}: {action}')

            elif client_address[0] == '192.168.41.242':  # Replace with the actual IP address of client 2
                # Handle data from client 2 (temperature)
                temperature = float(data)

                # Determine action based on temperature
                action = ""
                if temperature > 25:
                    action = "Buzzer On"
                else:
                    action = "Buzzer Off"

                # Update GUI for client 2 with received data and action
                update_gui(client2_label, None, temperature_label2, None, action_label2, client_address[0], None, temperature, None, action)

                # Send action to client 2
                client_socket.sendall(action.encode())
                logging.info(f'Sent action to {client_address[0]}: {action}')

    # Close the client socket
    client_socket.close()

# Function to update the GUI labels
def update_gui(client_label, intensity_label, temperature_label, humidity_label, action_label, client, intensity, temperature, humidity, action):
    client_label.SetLabel(f'Client: {client}')
    if intensity_label:
        intensity_label.SetLabel(f'Intensity: {intensity}')
    if temperature_label:
        temperature_label.SetLabel(f'Temperature: {temperature}')
    if humidity_label:
        humidity_label.SetLabel(f'Humidity: {humidity}')
    if action_label:
        action_label.SetLabel(f'Action: {action}')

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)
print(f'Server listening on {server_ip}:{server_port}')

# Create the wxPython GUI app
app = wx.App()

# Create the main frame
frame = wx.Frame(None, title="Server GUI")

# Create a main panel
panel = wx.Panel(frame)

# Create a sizer for the main panel
sizer = wx.BoxSizer(wx.HORIZONTAL)

# Create a sizer for client 1
client1_sizer = wx.BoxSizer(wx.VERTICAL)

# Create labels for client 1
client1_label = wx.StaticText(panel, label="Client 1:")
client1_label.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
client1_sizer.Add(client1_label, 0, wx.ALL, 10)
intensity_label1 = wx.StaticText(panel, label="Intensity:")
client1_sizer.Add(intensity_label1, 0, wx.ALL, 5)
action_label1 = wx.StaticText(panel, label="Action:")
client1_sizer.Add(action_label1, 0, wx.ALL, 5)

# Create a sizer for client 2
client2_sizer = wx.BoxSizer(wx.VERTICAL)

# Create labels for client 2
client2_label = wx.StaticText(panel, label="Client 2:")
client2_label.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
client2_sizer.Add(client2_label, 0, wx.ALL, 10)
temperature_label2 = wx.StaticText(panel, label="Temperature:")
client2_sizer.Add(temperature_label2, 0, wx.ALL, 5)
action_label2 = wx.StaticText(panel, label="Action:")
client2_sizer.Add(action_label2, 0, wx.ALL, 5)

# Create a stop button
stop_button = wx.Button(panel, label="Stop")
sizer.Add(stop_button, 0, wx.ALL, 10)

# Add the client sizers to the main sizer
sizer.Add(client1_sizer, 1, wx.EXPAND | wx.ALL, 10)
sizer.Add(client2_sizer, 1, wx.EXPAND | wx.ALL, 10)

# Set the main sizer for the panel
panel.SetSizer(sizer)

# Set the background color for the panel
panel.SetBackgroundColour(wx.Colour(240, 240, 240))

# Center the frame on the screen
frame.Center()

# Function to start the server in a separate thread
def start_server():
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Create a thread to start the server
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Function to handle the stop button event
def on_stop(event):
    # Close the server socket
    server_socket.close()

    # Destroy the GUI frame
    frame.Destroy()

    # Exit the application
    app.Exit()

# Bind the stop button event to the on_stop function
stop_button.Bind(EVT_BUTTON, on_stop)

# Show the frame
frame.Show()

# Run the wxPython event loop
app.MainLoop()
