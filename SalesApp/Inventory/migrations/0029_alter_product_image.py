# Generated by Django 4.1.6 on 2023-03-20 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0028_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Image',
            field=models.ImageField(blank=True, default='C:\\Users\\GaelIris\\GaelCoding\\BAppDev\\SalesApp\\static/pics/defproduct.jpg', upload_to='images/'),
        ),
    ]
