from queue import Full
from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt

# Initialize the Flask application
app = Flask(__name__)

pump_activated = False

PUMP_TOPIC = "pump"
BROKER = "35.239.200.114"
PORT = 1883

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")
        
mqtt_client.on_connect = on_connect
mqtt_client.connect(BROKER, PORT)        
mqtt_client.loop_start()


@app.route('/api/pump/activate', methods=['GET'])
def activatePump():
    global pump_activated
    
    if not pump_activated:
        mqtt_client.publish(PUMP_TOPIC, "ON")
        pump_activated = True
    else:
        return jsonify({"message": "Pump already activated!"})
    
    return jsonify({"message": "Pump activated!"})

@app.route('/api/pump/deactivate', methods=['GET'])
def deactivatePump():
    global pump_activated
    
    if pump_activated:
        mqtt_client.publish(PUMP_TOPIC, "OFF")
        pump_activated = False
    else:
        return jsonify({"message": "Pump already deactivated!"})
    
    return jsonify({"message": "Pump deactivated!"})

@app.route('/api/pump/status', methods=['GET'])
def pumpStatus():
    return jsonify({"pump_activated": pump_activated})

if __name__ == '__main__': 
    app.run(debug=True)