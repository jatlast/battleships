from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import vShipClass, vBattle
from .forms import ShipClassForm

# Create your views here.
def ship_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    ships = vShipClass.objects.all()
    return render(request, 'ships/ship_list.html', {'ships': ships})

def ship_detail(request, shipname):
    ship = get_object_or_404(vShipClass, shipname=shipname)
    return render(request, 'ships/ship_detail.html', {'ship': ship})

def ship_new(request):
    if request.method == "POST":
        form = ShipClassForm(request.POST)
        if form.is_valid():
            ship = form.save(commit=False)
            ship.author = request.user
            ship.date_updated = timezone.now()
#            ship.save()
            return redirect('ship_detail', shipname=ship.shipname)
    else:
        form = ShipClassForm()
        return render(request, 'ships/ship_edit.html', {'form': form})
