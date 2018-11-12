from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection, transaction
from django.http import HttpResponse
from django.utils import timezone
from .models import vShipClass, vBattle, ShipsLog
from .forms import ShipClassForm

#import sqlite3
#from sqlite3 import Error

# Create your views here.
def log_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    logs = ShipsLog.objects.all()
    return render(request, 'ships/log_list.html', {'logs': logs})

def ship_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    ships = vShipClass.objects.all()
    return render(request, 'ships/ship_list.html', {'ships': ships})

def ship_detail(request, shipname):
    ship = get_object_or_404(vShipClass, shipname=shipname)
    return render(request, 'ships/ship_detail.html', {'ship': ship})


@transaction.atomic # this function is a transaction...
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


@transaction.atomic # this function is a transaction & returns on errors...
def ship_edit(request, shipname):
    ship = get_object_or_404(vShipClass, shipname=shipname)
    
    # Not a POST -- Return
    if request.method != "POST":
        form = ShipClassForm(instance=ship)
        #return redirect('ship_detail', shipname=ship.shipname)
        return render(request, 'ships/ship_edit.html', {'form': form})
    # POST call -- Continue
    form = ShipClassForm(request.POST, instance=ship)

    log_message = ''
    error_message = ''
    msg_dict = {'form': form, 'ship': ship, 'log_message': log_message, 'error_message': error_message}

    # Not a valid form -- Return
    if form.is_valid() is False:
        error_message = f"{shipname}'s typeClass '{typeclass}' != bb|bc: {row} | {query_string}"
        msg_dict['error_message'] = error_message
        return render(request, 'ships/ship_edit.html', msg_dict)
#        return HttpResponse(mas_dict)

    # get the clean form values...
    shipname = form.cleaned_data['shipname']
    classname = form.cleaned_data['classname']
    launchyr = form.cleaned_data['launchyr']
    typeclass = form.cleaned_data['typeclass']
    country = form.cleaned_data['country']
    numguns = form.cleaned_data['numguns']
    bore = form.cleaned_data['bore']
    displacement = form.cleaned_data['displacement']
    # may use for logging...
    author = request.user
    updated = timezone.now()

    ship_exists = False
    class_exists = False

    # Not a valid Classes.typeClass -- Return
    if typeclass != 'bb' and typeclass != 'bc': # Mimics: CHECK (typeClass IN ('bb', 'bc')
        error_message = f"{shipname}'s typeClass '{typeclass}' != bb|bc"
        msg_dict['error_message'] = error_message
        return render(request, 'ships/ship_edit.html', msg_dict)
#        return HttpResponse(error_message)

    # Check if launchYr > battleYr
    with connection.cursor() as cursor:
        query_string = f"SELECT vs.shipName \
        FROM vShipClass vs \
        , vBattle vb \
        WHERE vs.shipName = vb.shipName \
        AND vs.shipName = '{shipname}' \
        AND {launchyr} > vb.battleYr;"
        cursor.execute(query_string)
        row = cursor.fetchone()
        # launchYr > battleYr -- return...
        if row is not None:
            error_message = f"{shipname}'s launch year > battle year: {row} | {query_string}"
            msg_dict['error_message'] = error_message
            return render(request, 'ships/ship_edit.html', msg_dict)
#
##########################################################################################################
    # Create SQL -- UPDATE TABLE Classes...
    with connection.cursor() as cursor:
        query_string = f"SELECT className FROM Classes WHERE className = '{classname}';"
        cursor.execute(query_string)
        row = cursor.fetchone()
        # shipName EXISTS so UPDATE...
        if row is not None:
            class_exists = True
            query_string = f"UPDATE Classes \
            SET typeclass = '{typeclass}' \
            , country = '{country}' \
            , numGuns = {numguns} \
            , bore = {bore} \
            , displacement = {displacement} \
            WHERE className = '{classname}';"
        else:
            class_exists = False
            query_string = f"INSERT INTO Classes (className, typeClass, country, numGuns, bore, displacement) \
            VALUES ('{classname}', '{typeclass}', '{country}', {numguns}, {bore}, {displacement});"
    try:
        # Begin (INSERT || UPDATE) into Classes TABLE...
        with connection.cursor() as cursor:
            cursor.execute(query_string)
            row = cursor.fetchone()
            # shipName EXISTS so UPDATE...
            if row is None:
                success_message = f"Success: shipClass {shipname} updated"
            else:
                error_message = f"Error: while creating or updating {shipname}'s information:  {row} | {query_string}"
#        msg_dict['error_message'] = error_message
#        return render(request, 'ships/ship_edit.html', msg_dict)

    except Exception as e:
        error_message = f"Exception {e}: while creating or updating {shipname}'s information:  {row} | {query_string}"
        msg_dict['error_message'] = error_message
        return render(request, 'ships/ship_edit.html', msg_dict)

###########################################################################################################
# Create SQL -- UPDATE TABLE Classes...
    with connection.cursor() as cursor:
        query_string = f"SELECT shipName FROM Ships WHERE shipName = '{shipname}';"
        cursor.execute(query_string)
        row = cursor.fetchone()
        # shipName EXISTS so UPDATE...
        if row is not None:
            ship_exists = True
            query_string = f"UPDATE Ships \
            SET shipClass = '{classname}' \
            , launchYr = {launchyr} \
            WHERE shipName = '{shipname}';"
        else:
            ship_exists = False
            query_string = f"INSERT INTO Ships (shipName, shipClass, launchYr) \
            VALUES ('{shipname}', '{classname}', {launchyr});"
            #error_message = f"The ship '{shipname}' already exists: {row} | {query_string}"
            #return HttpResponse(error_message)
        try:
            # Begin (INSERT || UPDATE) into Ships TABLE...
            with connection.cursor() as cursor:
                cursor.execute(query_string)
                row = cursor.fetchone()
                # shipName EXISTS so UPDATE...
                if row is None:
                    insert_new = True
                    success_message = success_message + f" | Success: Ship {shipname} updated"
                    
                    msg_dict['success_message'] = success_message
                    return render(request, 'ships/ship_edit.html', msg_dict)
                else:
                    insert_new = False
                    error_message = error_message + f" | Error: while creating or updating {shipname}'s information:  {row} | {query_string}"
                    msg_dict['error_message'] = error_message
                    return render(request, 'ships/ship_edit.html', msg_dict)
        except Exception as e:
            error_message = f"Exception {e}: while creating or updating {shipname}'s information:  {row} | {query_string}"
            msg_dict['error_message'] = error_message
            return render(request, 'ships/ship_edit.html', msg_dict)

###########################################################################################################

    # Repopulate the form with the new information...
#    form = ShipClassForm(instance=ship)
    #return redirect('ship_detail', shipname=ship.shipname)
    #return render(request, 'ships/ship_edit.html', {'form': form})
    msg_dict['success_message'] = success_message + " | Final exit. Final SQL:" + query_string 
    return render(request, 'ships/ship_edit.html', msg_dict)
