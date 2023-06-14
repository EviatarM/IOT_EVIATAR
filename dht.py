import time
import json
import random
import paho.mqtt.client as mqtt

# Define MQTT broker host, port, and topic
broker_host = "broker.hivemq.com"
broker_port = 1883
topic_dht = "smartparking/dht"

# Create MQTT client
client = mqtt.Client()

# Connect to MQTT broker
client.connect(broker_host, broker_port)

# DHT data producer
def publish_dht_data():
    while True:
        # Generate random temperature and humidity values
        temperature = random.uniform(20, 30)
        humidity = random.uniform(40, 60)

        # Create a JSON payload
        payload = {
            "temperature": temperature,
            "humidity": humidity
        }

        # Publish the payload to the MQTT broker
        client.publish(topic_dht, json.dumps(payload))

        # Wait for the next data update
        time.sleep(5)

# Start the MQTT loop in a separate thread
client.loop_start()

# Start the DHT data producer in a separate thread
import threading

dht_thread = threading.Thread(target=publish_dht_data)
dht_thread.start()