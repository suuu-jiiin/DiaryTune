# Generated by Django 5.1.3 on 2024-11-16 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryTune', '0004_alter_diary_activities_alter_diary_weather'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diary',
            old_name='weather',
            new_name='weathers',
        ),
    ]
