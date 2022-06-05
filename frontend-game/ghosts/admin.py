from django.contrib import admin

# Register your models here.
from .models import Hypervisor, GameMachine

admin.site.register(Hypervisor)
admin.site.register(GameMachine)