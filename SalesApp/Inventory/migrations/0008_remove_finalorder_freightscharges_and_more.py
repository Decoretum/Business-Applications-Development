# Generated by Django 4.1.6 on 2023-02-24 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0007_alter_finalorder_charges_alter_finalorder_finaldest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalorder',
            name='FreightsCharges',
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Collect',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
