import paho.mqtt.client as mqtt
from application_secrets import secrets
import time
import random
import json


# MQTT broker info
MQTT_BROKER_IP_ADDRESS = secrets.get("MQTT_BROKER_IP_ADDRESS")
MQTT_BROKER_PORT = secrets.get(
    "MQTT_BROKER_PORT"
)  # Use port 8883 for secure MQTT / # Default port for non-TLS HiveMQ connections is 1883
# USERNAME = secrets.get("USERNAME")
# PASSWORD = secrets.get("PASSWORD")
CLIENT_ID_PREFIX = "device"

# Define sensor groups and types
sensor_groups = [
    {"room": "home/office", "type": "temperature", "min": -20, "max": 50, "unit": ""},
    {"room": "home/bedroom", "type": "humidity", "min": 40, "max": 60, "unit": ""},
    {"room": "home/kitchen", "type": "air_quality", "min": 0, "max": 100, "unit": ""},
]


# MQTT connection callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{client._client_id.decode()} connected successfully 🎊🎊!")
    else:
        print(f"{client._client_id.decode()} failed to connect, return code {rc}\n")


def on_disconnect(client, userdata, rc):
    print(f"{client._client_id.decode()} disconnected, return code {rc}")


def on_publish(client, userdata, mid):
    print(f"{client._client_id.decode()} published message with id {mid}")


# Create and connect devices
devices = []
for i, sensor_group in enumerate(sensor_groups):
    client_id = f"{CLIENT_ID_PREFIX}-{i}-{sensor_group['room']}-{sensor_group['type']}"
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish  # Set the callback for when a message is published
    # client.username_pw_set(username=USERNAME, password=PASSWORD)
    # client.tls_set()  # Enable SSL/TLS support
    client.connect(MQTT_BROKER_IP_ADDRESS, MQTT_BROKER_PORT)
    devices.append({"client": client, "sensor_group": sensor_group})

# Start the MQTT client loop for each device
for device in devices:
    device["client"].loop_start()

# Publish sensor data
try:
    while True:
        for device in devices:
            sensor_group = device["sensor_group"]
            device_id = (
                device["client"]._client_id.decode().split("-")[1]
            )  # Extract the device ID from the client ID
            sensor_value = random.randint(sensor_group["min"], sensor_group["max"])
            payload = {sensor_group["type"]: f"{sensor_value}{sensor_group['unit']}"}
            payload_str = json.dumps(payload)
            result = device["client"].publish(
                f"{sensor_group['room']}/{sensor_group['type']}", payload_str
            )
            print(
                f"Publish result for {device['client']._client_id.decode()}: {result}"
            )  # Always print the result

            if result[0] != 0:
                print(
                    f"{device['client']._client_id.decode()} failed to publish message"
                )
            time.sleep(5)

except KeyboardInterrupt:
    print("Terminating...")

finally:
    # Stop the MQTT client loop and disconnect
    for device in devices:
        device["client"].loop_stop()
        device["client"].disconnect()
