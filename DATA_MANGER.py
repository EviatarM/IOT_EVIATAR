import time
import json
import random
import paho.mqtt.client as mqtt

# Define MQTT broker host, port, and topic
broker_host = "broker.hivemq.com"
broker_port = 1883
topic = "smartparking/updates"

# Define data storage folder
data_folder = "data form broker"

# Create MQTT client
client = mqtt.Client()

# Callback function for MQTT message received
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    data = json.loads(payload)
    door_status = data["door_status"]
    timestamp = data["timestamp"]
    # Write data to a file
    filename = f"{data_folder}/data_{timestamp}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

# Connect to MQTT broker and subscribe to the topic
client.connect(broker_host, broker_port)
client.subscribe(topic)
client.on_message = on_message

# Start the MQTT loop in a background thread
client.loop_start()

try:
    while True:
        # Generate random door status (open or closed)
        door_open = random.choice([True, False])

        # Create a JSON payload
        timestamp = int(time.time())
        payload = {
            "door_status": "open" if door_open else "closed",
            "timestamp": timestamp
        }

        # Publish the payload to the MQTT broker
        client.publish(topic, json.dumps(payload))

        # Wait for the next data update
        time.sleep(30)
except KeyboardInterrupt:
    # Disconnect from MQTT broker
    client.disconnect()
