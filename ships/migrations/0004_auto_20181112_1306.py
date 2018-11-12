# Generated by Django 2.1.3 on 2018-11-12 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0003_shipslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipslog',
            name='logid',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shipslog',
            name='inserted',
            field=models.DateTimeField(),
        ),
    ]
