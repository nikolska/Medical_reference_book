# Generated by Django 2.2.17 on 2021-03-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geographicalarea',
            name='image',
            field=models.ImageField(default=True, upload_to='media/geographical_area/'),
        ),
        migrations.AddField(
            model_name='organ',
            name='image',
            field=models.ImageField(default=True, upload_to='media/organs/'),
        ),
    ]