import paho.mqtt.client as mqtt
import json
import time
import threading

id = '20221702'
client_name = id + 'servidor'
client_telemetry_topic = id + '/telemetriaexame'
server_commands_topic = id + '/comandosexame'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

tempo_espera = 20   # 20 segundos

def send_led_command(client, state):
    command = json.dumps({'estado_led_on': state})
    print("Sending message:", command)
    client.publish(server_commands_topic, command)

def control_led(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

    send_led_command(client, True)
    time.sleep(tempo_espera)
    send_led_command(client, False)

    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['temp'] < 80:
        threading.Thread(target=control_led, args=(client,)).start()

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)