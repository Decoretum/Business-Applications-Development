# Generated by Django 4.1.6 on 2023-05-10 15:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0056_alter_finalorder_oceanvessel_alter_finalorder_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 10, 15, 57, 38, 287425, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Verification',
            field=models.CharField(blank=True, default='', max_length=13, unique=True),
        ),
    ]
