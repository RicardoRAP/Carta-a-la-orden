# Generated by Django 4.2 on 2023-05-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_dish_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='state2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Estado2'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='state',
            field=models.CharField(blank=True, choices=[('Amazonas', 'Amazonas'), ('Anzoátegui', 'Anzoátegui'), ('Apure', 'Apure'), ('Aragua', 'Aragua'), ('Barinas', 'Barinas'), ('Bolívar', 'Bolívar'), ('Carabobo', 'Carabobo'), ('Cojedes', 'Cojedes'), ('Delta Amacuro', 'Delta Amacuro'), ('Distrito Capital', 'Distrito Capital'), ('Falcón', 'Falcón'), ('Guárico', 'Guárico'), ('Lara', 'Lara'), ('Mérida', 'Mérida'), ('Miranda', 'Miranda'), ('Monagas', 'Monagas'), ('Nueva Esparta', 'Nueva Esparta'), ('Portuguesa', 'Portuguesa'), ('Sucre', 'Sucre'), ('Táchira', 'Táchira'), ('Trujillo', 'Trujillo'), ('Vargas', 'Vargas'), ('Yaracuy', 'Yaracuy'), ('Zulia', 'Zulia')], max_length=200, null=True, verbose_name='Estado'),
        ),
    ]