# Generated by Django 4.1.6 on 2023-02-24 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0004_alter_finalorder_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='BL',
            field=models.CharField(default=None, max_length=20, unique=True),
        ),
    ]