# Generated by Django 4.1.6 on 2023-03-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0018_alter_consignee_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
    ]