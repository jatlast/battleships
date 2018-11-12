from django import forms
from .models import vShipClass, vBattle

class ShipClassForm(forms.ModelForm):

    class Meta:
        model = vShipClass
        fields = ('shipname'
                  , 'classname'
                  , 'launchyr'
                  , 'typeclass'
                  , 'country'
                  , 'numguns'
                  , 'bore'
                  , 'displacement'
#                  , 'condition'
                  ,)
