# Generated by Django 2.1.3 on 2018-11-13 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0007_auto_20181113_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipslog',
            name='errtxt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]