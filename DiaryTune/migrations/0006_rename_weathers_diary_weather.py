# Generated by Django 5.1.3 on 2024-11-16 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryTune', '0005_rename_weather_diary_weathers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diary',
            old_name='weathers',
            new_name='weather',
        ),
    ]
