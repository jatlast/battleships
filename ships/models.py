# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models
from django.utils import timezone

# This is a VIEW...
class vShipClass(models.Model):
    country = models.CharField(db_column='country', max_length=15, blank=False, null=False)
    shipname = models.CharField(db_column='shipName', max_length=20, primary_key=True, blank=False, null=False)
    launchyr = models.IntegerField(db_column='launchYr', blank=False, null=False)
    classname = models.CharField(db_column='className', max_length=20, blank=False, null=False)
    typeclass = models.CharField(db_column='typeClass', max_length=2, blank=False, null=False)
    numguns = models.IntegerField(db_column='numGuns', blank=False, null=False)
    bore = models.IntegerField(db_column='bore', blank=False, null=False)
    displacement = models.IntegerField(db_column='displacement', blank=False, null=False)
    condition = models.CharField(db_column='condition', max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vShipClass'

    def __str__(self):
        return "%s %s %s" % (self.shipname, self.launchyr, self.classname)

    
# This is a VIEW...
class vBattle(models.Model):
    battleyr = models.IntegerField(db_column='battleYr', blank=False, null=False)
    battlename = models.CharField(db_column='battleName', max_length=20, primary_key=True, blank=False, null=False)
    shipname = models.CharField(db_column='shipName', max_length=20, blank=False, null=False)
    outcome = models.CharField(db_column='outcome', max_length=10, blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'vBattle'

    def __str__(self):
        return "%s %s %s" % (self.shipname, self.battlename, self.outcome)


# A logging table
class ShipsLog(models.Model):
    logid = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=32, blank=True, null=True)
    inserted = models.DateTimeField(blank=True, null=True)
    exceptxt = models.CharField(max_length=255, blank=True, null=True)
    querytxt = models.CharField(max_length=255, blank=True, null=True)
    msgtxt = models.CharField(max_length=255, blank=True, null=True)
    key1 = models.CharField(max_length=32, blank=True, null=True)
    val1 = models.CharField(max_length=32, blank=True, null=True)
    key2 = models.CharField(max_length=32, blank=True, null=True)
    val2 = models.CharField(max_length=32, blank=True, null=True)
    key3 = models.CharField(max_length=32, blank=True, null=True)
    val3 = models.CharField(max_length=32, blank=True, null=True)
    key4 = models.CharField(max_length=32, blank=True, null=True)
    val4 = models.CharField(max_length=32, blank=True, null=True)
    key5 = models.CharField(max_length=32, blank=True, null=True)
    val5 = models.CharField(max_length=32, blank=True, null=True)
        
    class Meta:
        managed = True
        db_table = 'ShipsLog'
                                                                                                

