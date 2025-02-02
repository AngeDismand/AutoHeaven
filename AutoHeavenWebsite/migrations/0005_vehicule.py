# Generated by Django 5.0.4 on 2024-04-30 21:32

import AutoHeavenWebsite.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoHeavenWebsite', '0004_tarif'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immatriculation', models.CharField(max_length=100)),
                ('marque', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('statut', models.CharField(choices=[('Disponilbe', 'Disponible'), ('Occupé', 'Occupé'), ('En attente', 'En attente')], max_length=12)),
                ('image', models.FileField(blank=True, null=True, upload_to=AutoHeavenWebsite.models.vehicule_directory_path)),
                ('category_vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoHeavenWebsite.categoryvehicule')),
            ],
        ),
    ]
