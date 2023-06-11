# Generated by Django 4.2 on 2023-06-11 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_rental_rentables_remove_rental_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('deliver_date', models.DateTimeField()),
                ('products', models.ManyToManyField(to='app.product')),
            ],
        ),
    ]
