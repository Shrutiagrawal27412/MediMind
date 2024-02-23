import paho.mqtt.client as mqtt
broker_address = "0.tcp.in.ngrok.io"
port = 19537     
mqtt_topic= 'heart-rate/#'
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(mqtt_topic)

# Callback when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(broker_address, port, 60)

mqtt_client.loop_start()
while not mqtt_client.is_connected():
    mqtt_client.publish("heart-rate/bpm", 1021)

mqtt_client.disconnect()
mqtt_client.loop_stop()
