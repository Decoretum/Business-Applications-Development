# Generated by Django 4.1.6 on 2023-05-11 06:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0061_alter_finalorder_time_alter_finalorder_voyage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 11, 6, 2, 33, 328281, tzinfo=datetime.timezone.utc)),
        ),
    ]
