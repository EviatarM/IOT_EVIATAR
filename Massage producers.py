import time
import json
import random
import paho.mqtt.client as mqtt

# Define MQTT broker host, port, and topic
broker_host = "broker.hivemq.com"
broker_port = 1883
topic = "smartparking/updates"

# Create MQTT client
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_host, broker_port)

# Publish door status to the smart parking broker
try:
    while True:
        # Get current timestamp
        timestamp = int(time.time())

        # Generate random door status (open or closed)
        door_open = random.choice([True, False])

        # Create a JSON payload
        payload = {
            "door_status": "open" if door_open else "closed",
            "timestamp": timestamp
        }

        # Publish the payload to the MQTT broker
        client.publish(topic, json.dumps(payload))

        # Print the published data
        print("Published:", payload)

        # Wait for the next data update
        time.sleep(60)
except KeyboardInterrupt:
    # Disconnect from MQTT broker
    client.disconnect()