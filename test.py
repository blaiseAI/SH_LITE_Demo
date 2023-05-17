# import paho.mqtt.client as mqtt
# import time
# import random
# import json


# # Number of devices to simulate
# NUM_DEVICES = 5

# # MQTT broker info
# MQTT_BROKER_IP_ADDRESS = "0466eb1a2b724e78bd7d90d597a225fd.s2.eu.hivemq.cloud"
# MQTT_BROKER_PORT = 8883  # Use port 8883 for secure MQTT
# USERNAME = "hivemq.webclient.1683737168672"
# PASSWORD = "7>n1f.?oKb9FREpD,0Bc"
# CLIENT_ID_PREFIX = "device"


# # MQTT connection callbacks
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print(f"{client._client_id.decode()} connected successfully!")
#     else:
#         print(f"{client._client_id.decode()} failed to connect, return code {rc}\n")


# def on_disconnect(client, userdata, rc):
#     print(f"{client._client_id.decode()} disconnected, return code {rc}")


# # New callback function for when a message is published
# def on_publish(client, userdata, mid):
#     print(f"{client._client_id.decode()} published message with id {mid}")


# # Create and connect devices
# devices = []
# for i in range(NUM_DEVICES):
#     client_id = f"{CLIENT_ID_PREFIX}-{i}"
#     client = mqtt.Client(client_id)
#     client.on_connect = on_connect
#     client.on_disconnect = on_disconnect
#     client.on_publish = on_publish  # Set the callback for when a message is published
#     client.username_pw_set(username=USERNAME, password=PASSWORD)
#     client.tls_set()  # Enable SSL/TLS support
#     client.connect(MQTT_BROKER_IP_ADDRESS, MQTT_BROKER_PORT)
#     devices.append(client)


# # Start the MQTT client loop for each device
# for device in devices:
#     device.loop_start()

# # Publish sensor data
# try:
#     while True:
#         for device in devices:
#             device_id = device._client_id.decode().split("-")[
#                 1
#             ]  # Extract the device ID from the client ID
#             temperature = random.randint(
#                 -20, 30
#             )  # Generate a random temperature between 20 and 30.
#             humidity = random.randint(
#                 40, 60
#             )  # Generate a random humidity between 40 and 60.
#             air_quality = random.randint(
#                 0, 100
#             )  # Generate a random air quality value between 0 and 100.
#             payload = {
#                 "temperature": f"{temperature}C",
#                 "humidity": f"{humidity}%",
#                 "airQuality": air_quality,
#             }
#             payload_str = json.dumps(payload)
#             result = device.publish(f"iot/sensor", payload_str)
#             if result[0] != 0:
#                 print(f"{device._client_id.decode()} failed to publish message")
#             time.sleep(1)

# except KeyboardInterrupt:
#     print("Terminating...")

# finally:
#     # Stop the MQTT client loop and disconnect
#     for device in devices:
#         device.loop_stop()
#         device.disconnect()
