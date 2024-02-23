import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
import requests
import paho.mqtt.client as mqtt
import json

CLIENT_ID = '23RR7Z'
CLIENT_SECRET = '87177074c3a3d23eeb4b5126be6409d4'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

fitbit_api_endpoint = "https://api.fitbit.com/1/user/9BGRDZ/activities/heart/date/today/1d/1min.json"

MQTT_BROKER = "0.tcp.in.ngrok.io"
MQTT_PORT = 10715
MQTT_TOPIC = "fitbit/heart_rate"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

def refresh_token(refresh_token):
    auth2_client.client.refresh_token(refresh_token)

def get_heart_rate_data():
    try:
        response = auth2_client.make_request(url=fitbit_api_endpoint)
        return response
    except fitbit.exceptions.HTTPUnauthorized:
        refresh_token(REFRESH_TOKEN)
        response = auth2_client.make_request(url=fitbit_api_endpoint)
        return response

heart_rate_data = get_heart_rate_data()
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()
while not mqtt_client.is_connected():
    mqtt_client.publish(MQTT_TOPIC, json.dumps(heart_rate_data))
mqtt_client.disconnect()
mqtt_client.loop_stop()
    
formatted_data = json.dumps({"heart_rate": heart_rate_data})
print(formatted_data)
