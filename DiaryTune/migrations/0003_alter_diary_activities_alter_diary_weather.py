# Generated by Django 4.2.16 on 2024-11-15 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiaryTune', '0002_diary_created_at_diary_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='activities',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='diary',
            name='weather',
            field=models.JSONField(default=list),
        ),
    ]
