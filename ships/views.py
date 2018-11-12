from django.shortcuts import render
from django.utils import timezone
from .models import vShipClass, vBattle

# Create your views here.
def ship_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    ships = vShipClass.objects.all()
    return render(request, 'ships/ship_list.html', {'ships': ships})

