import sys
import time
import json
import random
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt

# Define MQTT broker host, port, and topic
broker_host = "broker.hivemq.com"
broker_port = 1883
topic = "smartparking/updates"

# Create MQTT client
client = mqtt.Client()

# Create a custom QMainWindow for the main app window
class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main App")
        self.resize(400, 300)

        # Create a QLabel to display the data changes
        self.data_label = QLabel("Data changes will appear here")
        self.data_label.setAlignment(Qt.AlignCenter)

        # Create a QVBoxLayout to layout the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.data_label)

        # Create a QWidget to set the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(widget)

        # Connect to MQTT broker
        client.connect(broker_host, broker_port)

        # Subscribe to the MQTT topic
        client.subscribe(topic)
        client.on_message = self.on_message

        # Initialize the warning message box
        self.warning_box = None

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        data = json.loads(payload)
        door_status = data.get("door_status")

        # Update the data label with the door status
        self.data_label.setText(f"Door status: {door_status}")

        # Check for warning or alarm conditions
        if door_status == "open":
            self.show_warning("Door Open Warning", "The door is open!")
        elif door_status == "closed":
            self.hide_warning()

    def show_warning(self, title, message):
        # Show the warning message box if not already visible
        if self.warning_box is None or not self.warning_box.isVisible():
            self.warning_box = QMessageBox.warning(self, title, message)

    def hide_warning(self):
        # Hide the warning message box if visible
        if self.warning_box is not None and self.warning_box.isVisible():
            self.warning_box.hide()

# Create the QApplication
app = QApplication(sys.argv)

# Create an instance of the main app window
main_window = MainAppWindow()
main_window.show()

# Start the MQTT loop in a separate thread
client.loop_start()

# Run the application event loop
sys.exit(app.exec_())