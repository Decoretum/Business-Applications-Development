# Generated by Django 4.1.6 on 2023-04-02 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0043_alter_product_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalorder',
            name='Time',
            field=models.TimeField(default='8:00:01'),
        ),
    ]