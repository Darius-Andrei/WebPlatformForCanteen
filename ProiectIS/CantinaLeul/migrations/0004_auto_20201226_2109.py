# Generated by Django 3.1.3 on 2020-12-26 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CantinaLeul', '0003_newproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newproduct',
            old_name='image',
            new_name='imagine',
        ),
    ]
