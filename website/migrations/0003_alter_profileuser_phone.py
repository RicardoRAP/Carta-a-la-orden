# Generated by Django 4.2 on 2023-05-15 20:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_menu_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Coloque un número de teléfono válido.', regex='^\\+?\\d{11,15}$')], verbose_name='Número de télefono'),
        ),
    ]
