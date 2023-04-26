# Generated by Django 4.2 on 2023-04-26 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='new',
            field=models.BooleanField(default=True),
        ),
    ]
