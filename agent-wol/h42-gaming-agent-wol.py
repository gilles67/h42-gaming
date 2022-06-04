import sys, json, os.path, wakeonlan, logging, netifaces
import paho.mqtt.client as mqtt
logger = logging.getLogger('h42-gaming-wol-agent')

def config_json(filename="/opt/cloud/gaming/agent/agent-wol.json"):
    logger.info("Load configuration : %s ", filename)
    fd = open(filename)
    data = json.loaf(fd)
    fd.close()
    logger.debug("Configuration: %s", str(data))
    return data

def get_interface_ip(conf):
    adrs = netifaces.ifaddresses(conf['wol_interface'])
    iface = adrs[netifaces.AF_INET][0]
    conf['wol_interface_addr'] = iface['addr']
    logger.debug("Update interface address: %s", str(data))
    return conf

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code %s ", str(rc))
    client.subscribe("h42/gaming/wol")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    logger.info("Topic: %s, Data: %s", msg.topic, str(data))

    wakeonlan.send_magic_packet(data['mac'], interface=userdata['conf']['wol_interface_addr'])

def main(): 
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    conf = config_json()
    conf = get_interface_ip(conf)

    client = mqtt.Client(userdata={'conf': conf})
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(conf['mqtt_server'], 1883, 60)

    client.loop_forever()

if __name__ == "__main__":
    main()
