# Generated by Django 3.1.3 on 2020-12-27 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CantinaLeul', '0005_auto_20201227_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cos',
            name='codReferinta',
        ),
        migrations.RemoveField(
            model_name='cos',
            name='comandat',
        ),
        migrations.RemoveField(
            model_name='produscomandat',
            name='comandat',
        ),
    ]
