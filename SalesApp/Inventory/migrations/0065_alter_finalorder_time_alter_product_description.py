# Generated by Django 4.1.6 on 2023-07-20 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0064_alter_finalorder_time_alter_orderedproduct_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2023, 7, 20, 11, 52, 25, 872281, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.CharField(default=None, max_length=3000),
        ),
    ]
