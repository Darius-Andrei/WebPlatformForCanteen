# Generated by Django 3.1.3 on 2020-12-27 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CantinaLeul', '0010_auto_20201227_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='cos',
        ),
        migrations.AddField(
            model_name='cos',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CantinaLeul.newuser'),
        ),
    ]