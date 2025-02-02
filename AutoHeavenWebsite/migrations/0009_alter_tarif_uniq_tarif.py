# Generated by Django 5.0.4 on 2024-05-03 08:18

from django.db import migrations, models

def update_data_with_unique_values(apps, schema_editor):
        
        MyModel = apps.get_model('AutoHeavenWebsite', 'Tarif')

        instances = MyModel.objects.all()

        for instance in instances:
            instance.uniq_tarif = str(instance.category_vehicule) + '_' + str(instance.periodicite)
            instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AutoHeavenWebsite', '0008_alter_vehicule_marque_alter_vehicule_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarif',
            name='uniq_tarif',
            field=models.CharField(max_length=100,null=True),
        ),
          migrations.AlterField(
            model_name='categoryvehicule',
            name='libelle',
            field=models.CharField(max_length=100, unique=True),
        ),
        
         migrations.RunPython(update_data_with_unique_values),
    ]
