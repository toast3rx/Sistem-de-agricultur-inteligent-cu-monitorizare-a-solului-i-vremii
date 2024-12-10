import time
from machine import Pin, I2C
import PicoDHT22 as dht

dht_pin = machine.Pin(22)
rain_sensor = machine.ADC(26)
soil_sensor = machine.ADC(27)
light_pin = machine.Pin(21)

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

while True:
	temperature, humidity = dht_sensor.read()
	print("Temperature: ", temperature)
	print("Humidity: ", humidity)
	print("Raindrops: ", check_rain_status())
	print("Soil: ", check_soil_status())
	print("Light: ", check_light_status())
	print()
	time.sleep(2)
 