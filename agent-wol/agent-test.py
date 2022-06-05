import json
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect('2a0e:e701:1123:0020:7::1883', 1883, 60)
data={}
data["mac"] = "d8:bb:c1:02:32:4a"
client.publish("h42/gaming/wol", payload=json.dumps(data))