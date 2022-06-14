import zmq
from django.conf import settings
from django.core.signals import request_finished

class Agent:
    
    context = None
    socket = None
    bind = None
    error = False
    
    def define_ctx(self, bind):
        self.bind = bind
        self._create_ctx()

    def _create_ctx(self):
        self.context = zmq.Context()
        self.context.setsockopt(zmq.RCVTIMEO, 1000)
        self.context.setsockopt(zmq.SNDTIMEO, 1000)
        self.context.setsockopt(zmq.LINGER, 0)
        self.context.setsockopt(zmq.IPV6, True)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.bind)
    
    def _clear_ctx(self):
        self.error = False
        self.context.destroy()
        self.context = None
        self.socket = None

    def cmd(self, data):
        if not self.socket:
            self._create_ctx()
        self.socket.send_json(data)
        return self.socket.recv_json()


class agentWol(Agent):
    _current = None

    def __init__(self):
        self.define_ctx("tcp://{0}:6661".format(settings.AGENT_WOL))
        request_finished.connect(self._clear_cache)
        self.cache = {}

    def _clear_cache(self, **kwargs):
        if self.error:
            print("Clear Error: Reset Context")
            self._clear_ctx()
        print("Cache cleared: {0}".format(self.cache))
        self.cache.clear()

    def wakeonlan(self, mac):
        return self.cmd({"mac":mac, "cmd":"wakeonlan"})
       

    def ping(self, mac):
        if not 'ping' in self.cache:
            self.cache['ping'] = {}
        if not mac in self.cache['ping']:
            try:
                self.cache['ping'][mac] = self.cmd({"mac":mac, "cmd":"ping"})
            except Exception as err:
                self.error = True
                self.cache['ping'][mac] = None
        return self.cache['ping'][mac]

    @classmethod
    def current(cls): 
        if not cls._current: 
            cls._current = cls() 
        return cls._current

