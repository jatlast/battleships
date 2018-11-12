from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import vShipClass, vBattle

# Create your views here.
def ship_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    ships = vShipClass.objects.all()
    return render(request, 'ships/ship_list.html', {'ships': ships})

def ship_detail(request, shipname):
    ship = get_object_or_404(vShipClass, shipname=shipname)
    return render(request, 'ships/ship_detail.html', {'ship': ship})
