# Generated by Django 2.0.7 on 2018-08-21 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Interface',
            new_name='InterfaceProfile',
        ),
        migrations.AlterModelTable(
            name='interfaceprofile',
            table='interface_profile',
        ),
    ]
