# Generated by Django 4.0 on 2022-02-25 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messurementstation',
            old_name='Locaton',
            new_name='location',
        ),
    ]
