# Generated by Django 3.1.3 on 2020-12-27 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CantinaLeul', '0004_auto_20201226_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='job',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='r_password',
        ),
        migrations.AddField(
            model_name='newuser',
            name='produse',
            field=models.ManyToManyField(blank=True, to='CantinaLeul.newProduct'),
        ),
        migrations.CreateModel(
            name='produsComandat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comandat', models.BooleanField(default=False)),
                ('dataAdaugare', models.DateTimeField(auto_now=True)),
                ('dataComandare', models.DateTimeField(null=True)),
                ('produs', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CantinaLeul.newproduct')),
            ],
        ),
        migrations.CreateModel(
            name='cos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codReferinta', models.CharField(max_length=15)),
                ('comandat', models.BooleanField(default=False)),
                ('dataComandare', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CantinaLeul.newuser')),
                ('produse', models.ManyToManyField(to='CantinaLeul.produsComandat')),
            ],
        ),
    ]
