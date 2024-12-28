import time
from machine import Pin, I2C
import PicoDHT22 as dht
import simple as mqtt
import json
import network


dht_pin = machine.Pin(22)
rain_sensor = machine.ADC(26)
soil_sensor = machine.ADC(27)
light_pin = machine.Pin(21)


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
	
	# get unique id from rest api
	mqtt_server = "35.239.200.114"
 	
	client = mqtt.MQTTClient(client_id, mqtt_server)
	print("Client ID:", client_id)
	client.connect()
	print("Connected to MQTT")
	return client

def check_light_status():
    light_value = light_pin.value()
    
    if light_value == 0:
        return "Lumina"
    else:
        return "Intuneric"

def check_soil_status():
	raw_value = soil_sensor.read_u16() // 64
 
	if 0 <= raw_value < 256:
		return "Ud"
	elif 256 <= raw_value < 512:
		return "Umed"
	elif 512 <= raw_value < 768:
		return "Uscat"
	elif 768 <= raw_value <= 1023:
		return "Foarte uscat"
	else:
		return "Valoare necunoscuta"

def check_rain_status():
	raw_value = rain_sensor.read_u16() // 64
 
	if 0 <= raw_value < 256:
		return "Ploaie puternica"
	elif 256 <= raw_value < 512:
		return "Ploaie"
	elif 512 <= raw_value < 768:
		return "Ploaie inceata"
	elif 768 <= raw_value <= 1023:
		return "Nu ploua"
	else:
		return "Valoare necunoscuta"

dht_sensor = dht.PicoDHT22(dht_pin, None, False)
 
client_id = ""

wifi_connect()
client = mqtt_connect()

while True:
	try:
		temperature, humidity = dht_sensor.read()
		rain_status = check_rain_status()
		soil_status = check_soil_status()
		light_status = check_light_status()

		# Prepare the payload
		data = {
			"Temperatura (C)": temperature,
			"Umiditate(%)": humidity,
			"Vremea": rain_status,
			"Umiditate sol": soil_status,
			"Nivelul de lumina": light_status
		}
  
		temp_data = {
			"Temperatura (C)": temperature
		}
		hum_data = {
			"Umiditate(%)": humidity
		}
		rain_data = {
			"Vremea": rain_status
		}
		soil_data = {
			"Umiditate sol": soil_status
		}
		light_data = {
			"Nivelul de lumina": light_status
		}
  
		# Publish the data
		client.publish(client_id + "/temperature", json.dumps(temp_data))
		client.publish(client_id + "/humidity", json.dumps(hum_data))
		client.publish(client_id + "/rain", json.dumps(rain_data))
		client.publish(client_id + "/soil", json.dumps(soil_data))
		client.publish(client_id + "/light", json.dumps(light_data))


		# Convert to JSON and publish
		print("Published data:", data)

	except Exception as e:
		print("Error:", e)

	time.sleep(2)  # Delay before the next read