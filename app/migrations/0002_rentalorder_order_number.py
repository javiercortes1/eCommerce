# Generated by Django 4.2 on 2023-06-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalorder',
            name='order_number',
            field=models.IntegerField(default=5, unique=True),
            preserve_default=False,
        ),
    ]
