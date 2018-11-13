from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection, transaction
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from .models import vShipClass, vBattle, ShipsLog
from .forms import ShipClassForm
import inspect
from inspect import currentframe, getframeinfo

#import sqlite3
#from sqlite3 import Error

# Create your views here.
class ShipsLogView(generic.ListView):
    model = ShipsLog
    
#def log_list(request):
#    logs = ShipsLog.objects.all()
#    return render(request, 'ships/log_list.html', {'logs': logs})

def log_detail(request, logid):
    log = get_object_or_404(ShipsLog, logid=logid)
    return render(request, 'ships/log_detail.html', {'log': log})

def ship_list(request):
#    ships = vShipClass.objects.filter(order_by('shipname'))
    ships = vShipClass.objects.all()
    return render(request, 'ships/ship_list.html', {'ships': ships})

def ship_detail(request, shipname):
    ship = get_object_or_404(vShipClass, shipname=shipname)
    return render(request, 'ships/ship_detail.html', {'ship': ship})

#@transaction.atomic # this function is a transaction...
#def ship_new(request):
#    if request.method == "POST":
#        form = ShipClassForm(request.POST)
#        if form.is_valid():
#            ship = form.save(commit=False)
#            ship.author = request.user
#            ship.date_updated = timezone.now()
#            ship.save()
#            return redirect('ship_detail', shipname=ship.shipname)
#    else:
#        form = ShipClassForm()
#        return render(request, 'ships/ship_edit.html', {'form': form})

@transaction.atomic # this function is a transaction & returns on errors...
def ship_edit(request, shipname='UNK'):
    log_message = ''
    error_message = ''
    frameinfo = getframeinfo(currentframe())

    msg_dict = {'log_message': log_message, 'error_message': error_message}

    if shipname != 'UNK':
        ship = get_object_or_404(vShipClass, shipname=shipname)
        form = ShipClassForm(instance=ship)
        msg_dict['ship'] = ship
    else:
        form = ShipClassForm()
        author = ''
#        ship = 0
        ship = vShipClass()
#        ship = vShipClass.objects.get(shipname=shipname)

    msg_dict['logid'] = ShipsLog.objects.latest()
    author = request.user
    updated = timezone.now()

    # Not a POST -- Return
    if request.method != "POST":
#        form = ShipClassForm(instance=ship)
        msg_dict['form'] = form

        error_message = f"request.method({request.method}) != POST"
        msg_dict['error_message'] = error_message
        sl = ShipsLog.objects.latest()
        msg_dict['logid'] = int(sl.logid) + 1 
        ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                , msgtxt=msg_dict['error_message']
                                , key1='file', val1=frameinfo.filename
                                , key2='line', val2=inspect.stack()[0][2]
                                , key3='shipname', val3=shipname
                                , key4='method', val4=request.method)
        #return redirect('ship_detail', shipname=ship.shipname)
        return render(request, 'ships/ship_edit.html', msg_dict)

    # POST call -- Continue
    form = ShipClassForm(request.POST, instance=ship)

    msg_dict['form'] = form

    # Not a valid form -- Return
    if form.is_valid() is False:
        error_message = f"Invalid form form.is_valid({form.is_valid()})"
        msg_dict['error_message'] = error_message
        sl = ShipsLog.objects.latest()
        msg_dict['logid'] = int(sl.logid) + 1 
        ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                , msgtxt=msg_dict['error_message']
                                , key1='file', val1=frameinfo.filename
                                , key2='line', val2=inspect.stack()[0][2]
                                , key3='shipname', val3=shipname
                                , key4='is_valid', val4=form.is_valid())
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

    ship_exists = False
    class_exists = False

    # Not a valid Classes.typeClass -- Return
    if typeclass != 'bb' and typeclass != 'bc': # Mimics: CHECK (typeClass IN ('bb', 'bc')
        error_message = f"{shipname}'s typeClass '{typeclass}' != bb|bc"
        msg_dict['error_message'] = error_message

        sl = ShipsLog.objects.latest()
        msg_dict['logid'] = int(sl.logid) + 1 
        ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                , msgtxt=msg_dict['error_message']
                                , key1='file', val1=frameinfo.filename
                                , key2='line', val2=inspect.stack()[0][2]
                                , key3='shipname', val3=shipname
                                , key4='typeclass', val4=typeclass)

        return render(request, 'ships/ship_edit.html', msg_dict)

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
            error_message = f"{shipname}'s launch year > battle year"
            msg_dict['error_message'] = error_message

            sl = ShipsLog.objects.latest()
            msg_dict['logid'] = int(sl.logid) + 1 
            ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                    , msgtxt=msg_dict['error_message']
                                    , querytxt=query_string
                                    , key1='launchyr', val1=launchyr
                                    , key2='row', val2=row
                                    , key3='file', val3=frameinfo.filename
                                    , key4='line', val4=inspect.stack()[0][2]
                                    , key5='shipname', val5=shipname)
            return render(request, 'ships/ship_edit.html', msg_dict)

    ########## Classes Table ##########

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
                success_text = f"Success: shipClass {shipname} updated"
                msg_dict['success_text'] = success_text
                sl = ShipsLog.objects.latest()
                msg_dict['logid'] = int(sl.logid) + 1 
                ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                        , msgtxt = msg_dict['success_text']
                                        , querytxt=query_string
                                        , key1='file', val1=frameinfo.filename
                                        , key2='line', val2=inspect.stack()[0][2]
                                        , key3='shipname', val3=shipname
                                        , key4='classname', val4=classname
                                        , key5='row', val5=row)
            else:
                error_message = f"Error: while creating or updating shipClass {shipname}'s information"
                msg_dict['error_message'] = error_message

                sl = ShipsLog.objects.latest()
                msg_dict['logid'] = int(sl.logid) + 1 
                ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                        , msgtxt=msg_dict['error_message']
                                        , querytxt=query_string
                                        , key1='file', val1=frameinfo.filename
                                        , key2='line', val2=inspect.stack()[0][2]
                                        , key3='shipname', val3=shipname
                                        , key4='classname', val4=classname
                                        , key5='row', val5=row)

#    except sqlite3.Error as e:
#        msg_dict['exception_text'] = e

    except Exception as e:
        msg_dict['exception_text'] = e
#        if msg_dict['exception_text'] != 'success_message':
        error_message = f"Exception: while creating or updating shipClass {shipname}'s information"
        msg_dict['error_message'] = error_message
        sl = ShipsLog.objects.latest()
        msg_dict['logid'] = int(sl.logid) + 1 
        ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                , exceptxt=e
#                                , exceptxt=msg_dict['exception_text']
                                , msgtxt=msg_dict['error_message']
                                , querytxt=query_string
                                , key1='file', val1=frameinfo.filename
                                , key2='line', val2=inspect.stack()[0][2]
                                , key3='shipname', val3=shipname
                                , key4='row', val4=row)
        return render(request, 'ships/ship_edit.html', msg_dict)

    ########## Ships Table ##########

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

        try:
            # Begin (INSERT || UPDATE) into Ships TABLE...
            with connection.cursor() as cursor:
                cursor.execute(query_string)
                row = cursor.fetchone()
                # shipName EXISTS so UPDATE...
                if row is None:
                    insert_new = True
                    success_text = success_text + f" | Success: Ship {shipname} updated"                    
                    msg_dict['success_text'] = success_text
                    sl = ShipsLog.objects.latest()
                    msg_dict['logid'] = int(sl.logid) + 1
                    ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                            , msgtxt=msg_dict['success_text']
                                            , querytxt=query_string
                                            , key1='file', val1=frameinfo.filename
                                            , key2='line', val2=inspect.stack()[0][2]
                                            , key3='shipname', val3=shipname
                                            , key4='row', val4=row)
                    return render(request, 'ships/ship_edit.html', msg_dict)
                else:
                    insert_new = False
                    error_message = error_message + f" | Error: while creating or updating {shipname}'s info."
                    msg_dict['error_message'] = error_message
                    sl = ShipsLog.objects.latest()
                    msg_dict['logid'] = int(sl.logid) + 1
                    ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                            , msgtxt=msg_dict['error_message']
                                            , querytxt=query_string
                                            , key1='file', val1=frameinfo.filename
                                            , key2='line', val2=inspect.stack()[0][2]
                                            , key3='shipname', val3=shipname
                                            , key4='row', val4=row)
                    return render(request, 'ships/ship_edit.html', msg_dict)
        except Exception as e:
            error_message = f"Exception: while creating or updating {shipname}'s information"
            msg_dict['error_message'] = error_message
            msg_dict['exception_text'] = e
            sl = ShipsLog.objects.latest()
            msg_dict['logid'] = int(sl.logid) + 1
            ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                    , exceptxt=msg_dict['exception_text']
                                    , msgtxt=msg_dict['error_message']
                                    , querytxt=query_string
                                    , key1='file', val1=frameinfo.filename
                                    , key2='line', val2=inspect.stack()[0][2]
                                    , key3='shipname', val3=shipname
                                    , key4='row', val4=row)
            return render(request, 'ships/ship_edit.html', msg_dict)

        
    ########## Ships Table (with same name as the new class) ##########
    if not class_exists and not ship_exists: 
        query_string = query_string + f"INSERT INTO Ships (shipName, shipClass)\
                                        VALUES ('{classname}', '{classname}');"
        try:
            # Begin INSERT into Ships TABLE...
            with connection.cursor() as cursor:
                cursor.execute(query_string)
                row = cursor.fetchone()
                # INSERT success...
                if row is None:
                    insert_new = True
                    success_text = success_text + f" | Success: Dummy Ship {classname} inserted to match new  class"
                    
                    msg_dict['success_text'] = success_text
                    sl = ShipsLog.objects.latest()
                    msg_dict['logid'] = int(sl.logid) + 1
                    ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                            , msgtxt=msg_dict['success_text']
                                            , querytxt=query_string
                                            , key1='file', val1=frameinfo.filename
                                            , key2='line', val2=inspect.stack()[0][2]
                                            , key3='classname', val3=shipname
                                            , key4='row', val4=row)
                    return render(request, 'ships/ship_edit.html', msg_dict)
                else:
                    insert_new = False
                    error_message = error_message + error_message + f" | Error: inserting dummy class-matching ship {classname}"
                    msg_dict['error_message'] = error_message
                    sl = ShipsLog.objects.latest()
                    msg_dict['logid'] = int(sl.logid) + 1
                    ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                            , msgtxt=msg_dict['error_message']
                                            , querytxt=query_string
                                            , key1='file', val1=frameinfo.filename
                                            , key2='line', val2=inspect.stack()[0][2]
                                            , key3='shipname', val3=shipname
                                            , key4='row', val4=row)
                    return render(request, 'ships/ship_edit.html', msg_dict)
        except Exception as e:
            error_message = f"Exception: while creating or updating {shipname}'s information"
            msg_dict['error_message'] = error_message
            msg_dict['exception_text'] = e
            sl = ShipsLog.objects.latest()
            msg_dict['logid'] = int(sl.logid) + 1
            ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                                    , exceptxt=msg_dict['exception_text']
                                    , msgtxt=msg_dict['error_message']
                                    , querytxt=query_string
                                    , key1='file', val1=frameinfo.filename
                                    , key2='line', val2=inspect.stack()[0][2]
                                    , key3='shipname', val3=shipname
                                    , key4='row', val4=row)
            return render(request, 'ships/ship_edit.html', msg_dict)

        
    # Getting here should indicate all INSERTs and/or UPDATEs were successful
    msg_dict['success_text'] = msg_dict['success_text'] + " | Final exit. " + msg_dict['error_message']

    sl = ShipsLog.objects.latest()
    msg_dict['logid'] = int(sl.logid) + 1
    ShipsLog.objects.create(logid=msg_dict['logid'], author=author, inserted=updated
                            , msgtxt=msg_dict['error_message']
                            , querytxt=query_string
                            , key1='file', val1=frameinfo.filename
                            , key2='line', val2=inspect.stack()[0][2]
                            , key3='shipname', val3=shipname
                            , key4='row', val4=row)
    return render(request, 'ships/ship_edit.html', msg_dict)
