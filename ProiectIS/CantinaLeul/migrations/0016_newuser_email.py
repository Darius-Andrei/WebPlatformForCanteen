# Generated by Django 3.1.3 on 2021-01-05 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CantinaLeul', '0015_auto_20210105_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
