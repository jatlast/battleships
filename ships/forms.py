from django import forms
from .models import vShipClass, vBattle

class ShipClassForm(forms.ModelForm):
#    shipname = forms.CharField(max_length=20) # Handled automatically by Django

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
