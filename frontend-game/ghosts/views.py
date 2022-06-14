import json
import paho.mqtt.client as mqtt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import GameMachine

@login_required
def index(request):
    gm_list = GameMachine.objects.filter(owner_id=request.user.id)
    context = {'game_machine_list': gm_list, 'name': 'Home'}
    return render(request, 'home.html', context)

@login_required
def machine(request, machine_id):
    gms = GameMachine.objects.filter(owner_id=request.user.id, id=machine_id)
    gm = None
    if len(gms) > 0:
        gm = gms[0]

    context = {'gm': gm, 'name': 'Machine'}
    return render(request, 'machine.html', context)

@login_required
def machine_cmd(request, machine_id, machine_cmd):
    gms = GameMachine.objects.filter(owner_id=request.user.id, id=machine_id)
    gm = None
    if len(gms) > 0:
        gm = gms[0]




    if gm:
        if machine_cmd == 'hypervisor_wol':
            gm.host.wol_start()
        return redirect('/gaming/machine/{0}/'.format(gm.id))
    else:
        return redirect('/')



def publish_mqtt(topic, data):
    client = mqtt.Client()
    client.connect(settings.MQTT_SERVER, 1883, 60)
    client.publish(topic, payload=json.dumps(data))
