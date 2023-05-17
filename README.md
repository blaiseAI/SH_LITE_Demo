# MQTT Sensor Simulator

This program simulates multiple MQTT devices, each of which generates sensor data and publishes it to a specific topic. The sensor data are generated randomly within defined limits.

## Requirements

You need Python 3.7 or higher to run this program. Also, you need to install the following Python packages:

- paho-mqtt
- application_secrets

You can install these packages using pip:

`pip install paho-mqtt`
`pip install application_secrets`


You also need an MQTT broker to publish the sensor data. The broker's IP address and port are defined in the `application_secrets.py` file.

## Configuration

The program uses a list of sensor groups for configuration. Each group defines the room (topic), sensor type, and range of possible values. You can adjust these settings in the `sensor_groups` variable in the program.

The MQTT broker's IP address and port are fetched from a `secrets` dictionary, which is expected to be in a module named `application_secrets`.

Here is an example of what the `application_secrets.py` file might look like:

```python
secrets = {
    "MQTT_BROKER_IP_ADDRESS": "192.168.1.100",
    "MQTT_BROKER_PORT": 1883
}
```

## Running the Program
You can run the program from the command line:

`python mqtt_sensor_simulator.py`

This will start the MQTT clients, connect them to the broker, and start publishing sensor data.

The program will continue to run until it is interrupted with a keyboard interrupt (Ctrl+C). When it is interrupted, it will disconnect the MQTT clients and stop.

## Output
The program prints the status of the MQTT clients and the results of the publish operations. If a client successfully connects, it will print a message indicating this. Similarly, if a client disconnects or fails to connect, it will print a message.

When a message is published, the program prints the result of the publish operation. If the publish operation is successful, it will print the message ID. If the publish operation fails, it will print an error message.