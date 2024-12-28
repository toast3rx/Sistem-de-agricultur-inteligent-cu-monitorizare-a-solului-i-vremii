import simple as mqtt
import network
import time
from machine import Pin

API_URL = "http://localhost:5000"
mqtt_server = "35.239.200.114"
port = 1883
topic = "pump"
client_id = "actuator"

pump_motor = Pin(16, Pin.OUT)


def wifi_connect():

	ssid = "Alex"
	password = "kamikaze"

	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)

	mac =  wlan.config('mac')
	global client_id
	client_id = "pico-" + "".join("{:02x}".format(x) for x in mac)

	wlan.connect(ssid, password)

	while not wlan.isconnected():
		time.sleep(1)
		print("Connecting to WiFi...")

	print("Connected to WiFi")

def mqtt_connect():
	client = mqtt.MQTTClient(client_id, mqtt_server)
	print("Client ID:", client_id)
	client.connect()
	print("Connected to MQTT")
	return client

def mqtt_callback(topic, msg):
	msg = msg.decode()
	topic = topic.decode()

	if (topic == "pump"):
		if (msg == "ON"):
			pump_motor.value(1)
		elif (msg == "OFF"):
			pump_motor.value(0)


wifi_connect()
client = mqtt_connect()
client.set_callback(mqtt_callback)

client.subscribe(topic)

try:
	while True:
		client.check_msg()
		time.sleep(1)
except KeyboardInterrupt:
	print("Disconnecting...")
	client.disconnect()
