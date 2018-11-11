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

class Classes(models.Model):
#    classname = models.TextField(db_column='className', unique=True, blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    classname = models.TextField(db_column='className', primary_key=True, blank=False, null=False)  # JTB Edited
    typeclass = models.CharField(db_column='typeClass', max_length=2, blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(blank=True, null=True)  # This field type is a guess.
    numguns = models.IntegerField(db_column='numGuns', blank=True, null=True)  # Field name made lowercase.
    bore = models.IntegerField(blank=True, null=True)
    displacement = models.IntegerField(blank=True, null=True)
    # NOTE: not implemented
         # CONSTRAINT CHECK (typeClass IN ('bb', 'bc'))

    class Meta:
        managed = False
        db_table = 'Classes'

    def __str__(self):
        return "%s %s" % (self.classname, self.typeclass)
    

class Ships(models.Model):
    shipname = models.TextField(db_column='shipName', primary_key=True, blank=False, null=False)  # Field name made lowercase. This field type is a guess.
#    shipclass = models.TextField(db_column='shipClass', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    shipclass = models.ForeignKey(Classes, on_delete=models.CASCADE)  # JTB Edited
    launchyr = models.IntegerField(db_column='launchYr', blank=True, null=True)  # Field name made lowercase.
    # NOTE: not implemented
         # ?? CONSTRAINT fkClasses FOREIGN KEY (shipClass) REFERENCES Classes (className)
         # 

    class Meta:
        managed = False
        db_table = 'Ships'

    def __str__(self):
        return "%s %s" % (self.shipname, self.shipclass)

        
class Battles(models.Model):
    battlename = models.TextField(db_column='battleName', primary_key=True, blank=False, null=False)  # Field name made lowercase. This field type is a guess.
    battleyr = models.IntegerField(db_column='battleYr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Battles'

    def __str__(self):
        return "%s %s" % (self.battlename, self.battleyr)


class Outcomes(models.Model):
    ship = models.ForeignKey(Ships, on_delete=models.CASCADE)  # This field type is a guess.
    battle = models.ForeignKey(Battles, on_delete=models.CASCADE)  # This field type is a guess.
    outcome = models.TextField(db_column='outcome', blank=True, null=True)  # This field type is a guess.
    # NOTE: not implemented
         # CONSTRAINT CHECK (outcome IN ('sunk', 'ok', 'damaged'))
         # ?? CONSTRAINT fkShips FOREIGN KEY (ship) REFERENCES Ships (shipName),
         # ?? CONSTRAINT fkBattles FOREIGN KEY (battle) REFERENCES Battles (battleName)

    class Meta:
        managed = False
        db_table = 'Outcomes'
        unique_together = (('ship', 'battle'),)

    def __str__(self):
        return "%s %s %s" % (self.ship, self.battle, self.outcome)


