# Generated by Django 5.0.4 on 2024-05-16 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_driver_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='level',
            field=models.CharField(choices=[('Artiste du Volant', 'Artiste du Volant'), ('Maitre Conducteur', 'Maitre Conducteur'), ('Expert au Volant', 'Expert au Volant')], max_length=20, null=True),
        ),
    ]