# Generated by Django 4.1.6 on 2023-02-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0013_alter_finalorder_placedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consignee',
            name='PortDischarge',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
