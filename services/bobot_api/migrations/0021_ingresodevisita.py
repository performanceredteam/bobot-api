# Generated by Django 4.2 on 2023-04-26 19:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0020_visitantedatos'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngresoDeVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iv_fecha', models.DateField(default=django.utils.timezone.now)),
                ('vd_cedula', models.PositiveBigIntegerField()),
            ],
        ),
    ]
