# Generated by Django 5.0.4 on 2024-04-30 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoHeavenWebsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Employé', 'Employé'), ('Client', 'Client'), ('SuperAdmin', 'SuperAdmin')], max_length=10),
        ),
    ]
