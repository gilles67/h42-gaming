import uuid
from django.db import models
from django.conf import settings
from .utils.agents import agentWol


class Hypervisor(models.Model):
    name = models.CharField(max_length=128)
    mac = models.CharField(max_length=20)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

    @property
    def wol_status(self):
        agent = agentWol.current()
        return agent.ping(self.mac)

    def wol_start(self):
        agent = agentWol.current()
        return agent.wakeonlan(self.mac)

class GameMachine(models.Model):
    host = models.ForeignKey(Hypervisor, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    uuid = models.UUIDField()

    def __str__(self):
        return "{1} @ {0}".format(self.host.name, self.name)

