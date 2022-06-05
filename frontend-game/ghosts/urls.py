from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('machine/<int:machine_id>/', views.machine, name='machine_preview'),
    path('machine/<int:machine_id>/<str:machine_cmd>', views.machine_cmd, name='machine_cmd'),
]