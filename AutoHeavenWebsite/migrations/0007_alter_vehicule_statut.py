# Generated by Django 5.0.4 on 2024-05-01 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoHeavenWebsite', '0006_alter_vehicule_immatriculation_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicule',
            name='statut',
            field=models.CharField(choices=[('Disponible', 'Disponible'), ('Occupé', 'Occupé'), ('En attente', 'En attente')], max_length=12),
        ),
    ]
