# Generated by Django 4.1.6 on 2023-02-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0008_remove_finalorder_freightscharges_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='BL',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
