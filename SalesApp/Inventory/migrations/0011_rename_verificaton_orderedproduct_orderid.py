# Generated by Django 4.1.6 on 2023-02-24 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0010_alter_finalorder_notifyname_alter_finalorder_shipper_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderedproduct',
            old_name='Verificaton',
            new_name='OrderID',
        ),
    ]