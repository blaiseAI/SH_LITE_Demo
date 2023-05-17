import json
import random
import time
import paho.mqtt.client as mqtt
from application_secrets import secrets

# MQTT broker info
MQTT_BROKER_IP_ADDRESS = secrets.get("MQTT_BROKER_IP_ADDRESS")
MQTT_BROKER_PORT = secrets.get("MQTT_BROKER_PORT")
CLIENT_ID_PREFIX = "device"

# Define sensor groups and types
sensor_groups = [
    {"room": "home/office", "type": "temperature", "min": -20, "max": 50, "unit": ""},
    {"room": "home/bedroom", "type": "humidity", "min": 40, "max": 60, "unit": ""},
    {"room": "home/kitchen", "type": "air_quality", "min": 0, "max": 100, "unit": ""},
]


# MQTT connection callbacks
def on_connect(client, userdata, flags, rc):
    print(
        f"{client._client_id.decode()} connected successfully!"
        if rc == 0
        else f"{client._client_id.decode()} failed to connect, return code {rc}"
    )


def on_disconnect(client, userdata, rc):
    print(f"{client._client_id.decode()} disconnected, return code {rc}")


def on_publish(client, userdata, mid):
    print(f"{client._client_id.decode()} published message with id {mid}")


def create_and_connect_devices(sensor_groups):
    devices = []
    for i, sensor_group in enumerate(sensor_groups):
        client_id = (
            f"{CLIENT_ID_PREFIX}-{i}-{sensor_group['room']}-{sensor_group['type']}"
        )
        client = mqtt.Client(client_id)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish
        client.connect(MQTT_BROKER_IP_ADDRESS, MQTT_BROKER_PORT)
        devices.append({"client": client, "sensor_group": sensor_group})
    return devices


def start_devices(devices):
    for device in devices:
        device["client"].loop_start()


def publish_sensor_data(devices):
    try:
        while True:
            for device in devices:
                sensor_group = device["sensor_group"]
                device_id = device["client"]._client_id.decode().split("-")[1]
                sensor_value = random.randint(sensor_group["min"], sensor_group["max"])
                payload = {
                    sensor_group["type"]: f"{sensor_value}{sensor_group['unit']}"
                }
                payload_str = json.dumps(payload)
                result = device["client"].publish(
                    f"{sensor_group['room']}/{sensor_group['type']}", payload_str
                )
                print(
                    f"Publish result for {device['client']._client_id.decode()}: {result}"
                )
                if result[0] != 0:
                    print(
                        f"{device['client']._client_id.decode()} failed to publish message"
                    )
                time.sleep(5)
    except KeyboardInterrupt:
        print("Terminating...")
        cleanup(devices)


def cleanup(devices):
    for device in devices:
        device["client"].loop_stop()
        device["client"].disconnect()


if __name__ == "__main__":
    devices = create_and_connect_devices(sensor_groups)
    start_devices(devices)
    publish_sensor_data(devices)
