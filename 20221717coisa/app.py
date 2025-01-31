from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt
from counterfit_shims_grove.grove_led import GroveLed
import json

sensor = DHT("11", 1)
led=GroveLed(4)

id = '20221717'

client_name = id + 'coisa'
client_telemetry_topic = id + '/telemetriaexame'
server_command_topic = id + '/commandosexame'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("MQTT connected!")

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['estado_led_on']:
        led.on()
    else:
        led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    _, valortemperatura = sensor.read()
    telemetry = json.dumps({'temp' : valortemperatura})
    print("Sending telemetry:", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
