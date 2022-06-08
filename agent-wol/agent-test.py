import json, zmq
#import paho.mqtt.client as mqtt

context = zmq.Context()
context.setsockopt(zmq.RCVTIMEO, 1000)
context.setsockopt(zmq.SNDTIMEO, 1000)
context.setsockopt(zmq.LINGER, 0)
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:6661")

socket.send_json({"mac":"d8:bb:c1:02:32:4a", "query":"wakeonlan"})
print(socket.recv_json())

socket.send_json({"mac":"d8:bb:c1:02:32:4a", "query":"ping"})
print(socket.recv_json())

#socket.close()