import sys, json, os.path, wakeonlan, logging, netifaces, time, socket
from icmplib import ping
from netaddr import EUI
from http.server import BaseHTTPRequestHandler, HTTPServer
logger = logging.getLogger('h42-gaming-wol-agent')

class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6

class RCPServer(BaseHTTPRequestHandler):
    _helper = None

    def do_GET(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/text')
        self.end_headers()
        self.wfile.write('Bad request ! GET : {0}'.format(self.path).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        res = RCPServer._helper._cmd(body)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())

    @classmethod
    def setHelper(cls, helper):
        cls._helper = helper

class RPCHelper:

    def __init__(self, userdata=None):
        self.conf = {}
        self.functions = {}
        self.userdata = userdata

    def register(self, cmd_name, function):
        self.functions[cmd_name] = function

    def _cmd(self, req):
        if 'cmd' in req: 
            if req['cmd'] in self.functions: 
                res = self.functions[req['cmd']](req, userdata=self.userdata)
                if not res:
                    res = {'error': 'no function returns'}
                return res

def config_json(filename="/opt/cloud/gaming/agent/agent-wol.json"):
    logger.info("Load configuration : %s ", filename)
    fd = open(filename)
    data = json.load(fd)
    fd.close()
    logger.debug("Configuration: %s", str(data))
    return data

def get_interface_ip(conf):
    adrs = netifaces.ifaddresses(conf['wol_interface'])
    iface = adrs[netifaces.AF_INET][0]
    conf['wol_interface_addr'] = iface['addr']
    logger.debug("Update interface address: %s", str(conf))
    return conf

def on_wakeonlan(req, userdata):
    logger.info("on wakeonlan Data: %s", str(req))
    wakeonlan.send_magic_packet(req['mac'], interface=userdata['conf']['wol_interface_addr'])
    userdata.update({'status': { req['mac']: 'starting'}})
    logger.debug("userdata: %s", str(userdata))
    req['status'] = userdata['status'][req['mac']]
    return req

def on_ping(req, userdata):
    logger.info("on ping Data: %s", str(req))
    mac = EUI(req['mac'])
    ip = mac.ipv6_link_local()
    logger.debug("ipv6: %s", str(ip))

    host =  ping(str(ip), count=1)
    req ['is_alive'] = host.is_alive
    req ['avg_rtt'] = host.avg_rtt

    if host.is_alive:
        userdata.update({'status': { req['mac']: 'ok'}})
    elif 'status' in userdata:
        if req['mac'] in userdata['status']:
            if userdata['status'][req['mac']] == 'starting':
                userdata.update({'status': { req['mac']: 'starting'}})
        else:
            userdata.update({'status': { req['mac']: 'poweroff'}})    
    else:
        userdata.update({'status': { req['mac']: 'poweroff'}})

    req['status'] = userdata['status'][req['mac']]
    logger.debug("userdata: %s", str(userdata))
    return req


def main(): 
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    conf = config_json()
    conf = get_interface_ip(conf)

    rpc = RPCHelper(userdata={'conf': conf})
    rpc.register('wakeonlan', on_wakeonlan)
    rpc.register('ping', on_ping)

    RCPServer.setHelper(rpc)
    webServer = HTTPServerV6(('::', 6661), RCPServer)

    try:
        logger.info("H42 Gaming WoL Agent Started")
        webServer.serve_forever()
    except KeyboardInterrupt:
        logger.info("H42 Gaming WoL Agent Stopped")
        pass

if __name__ == "__main__":
    main()
