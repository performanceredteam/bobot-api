# Generated by Django 4.2 on 2023-04-23 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0014_alter_apartamentoph_ph_apartamento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacaVehiculoVisita',
            fields=[
                ('pl_placa', models.CharField(max_length=7, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
