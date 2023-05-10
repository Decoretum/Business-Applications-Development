# Generated by Django 4.1.6 on 2023-05-10 16:46

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0057_alter_finalorder_time_alter_finalorder_verification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Color',
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Charges',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Time',
            field=models.TimeField(default=datetime.datetime(2023, 5, 10, 16, 46, 21, 551167, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notifyparty',
            name='Name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.CharField(default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='GrossWeight',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
