# Generated by Django 4.1.6 on 2023-02-24 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0009_alter_finalorder_bl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalorder',
            name='NotifyName',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.notifyparty'),
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Shipper',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.company'),
        ),
        migrations.AlterField(
            model_name='finalorder',
            name='Verification',
            field=models.CharField(blank=True, default=None, max_length=13, null=True, unique=True),
        ),
    ]
