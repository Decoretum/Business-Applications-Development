# Generated by Django 4.1.6 on 2023-02-23 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_remove_finalorder_marks_remove_finalorder_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
