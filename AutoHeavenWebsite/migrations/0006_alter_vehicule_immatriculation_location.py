# Generated by Django 5.0.4 on 2024-05-01 08:52

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoHeavenWebsite', '0005_vehicule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicule',
            name='immatriculation',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_libelle', models.CharField(max_length=500)),
                ('date_debut', models.DateField(verbose_name='date de début')),
                ('date_fin', models.DateField(verbose_name='date de fin')),
                ('montant_total', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('statut', models.CharField(choices=[('Payé', 'Payé'), ('En attente', 'En attente')], max_length=12)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoHeavenWebsite.vehicule')),
            ],
        ),
    ]
