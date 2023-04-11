# Generated by Django 4.1.6 on 2023-03-20 12:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0033_alter_finalorder_totalcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='TotalCost',
            field=models.FloatField(default=0, validators=[django.core.validators.DecimalValidator(10, 2)]),
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='totalcost',
            field=models.FloatField(default=0, validators=[django.core.validators.DecimalValidator(10, 2)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='Cost',
            field=models.FloatField(default=0, validators=[django.core.validators.DecimalValidator(5, 2)]),
        ),
    ]