# Generated by Django 4.2 on 2023-04-21 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApartamentoPh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_propietario', models.CharField(max_length=50)),
                ('ph_telefono', models.CharField(max_length=12)),
                ('ph_mail', models.EmailField(max_length=254)),
                ('ph_torre', models.PositiveSmallIntegerField(null=True)),
                ('ph_apartamento', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
