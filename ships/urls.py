from django.urls import path
from . import views

urlpatterns = [
    path('', views.ship_list, name='ship_list'),
]
