import sys
import time
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import paho.mqtt.client as mqtt

# Define MQTT broker host, port, and topic
broker_host = "broker.hivemq.com"
broker_port = 1883
topic = "smartparking/updates"

# Create MQTT client
client = mqtt.Client()

# Door status label text
door_status_text = ""

# Callback function for MQTT message received
def on_message(client, userdata, msg):
    global door_status_text
    payload = msg.payload.decode("utf-8")
    data = json.loads(payload)
    door_status = data["door_status"]
    door_status_text = door_status

# Connect to MQTT broker and subscribe to the topic
client.connect(broker_host, broker_port)
client.subscribe(topic)
client.on_message = on_message

# Create the GUI window
app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(100, 100, 300, 200)
window.setWindowTitle("Door Status")

# Door status label
label = QLabel(window)
label.setGeometry(50, 50, 200, 50)
label.setText("Press the button to get door status")

# Button click event handler
def button_clicked():
    global door_status_text
    label.setText("Door Status: " + door_status_text)

# Button
button = QPushButton("Get Door Status", window)
button.setGeometry(100, 120, 100, 30)
button.clicked.connect(button_clicked)

# Show the GUI window
window.show()

# Start the MQTT loop in a background thread
client.loop_start()

# Start the application event loop
sys.exit(app.exec_())