# Generated by Django 4.2 on 2023-04-26 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0017_ingresosalidavehiculovisita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresosalidavehiculovisita',
            name='vi_fecha_hora_ingreso',
            field=models.DateTimeField(verbose_name='%Y-%m-%d %H:%M:%s'),
        ),
        migrations.AlterField(
            model_name='ingresosalidavehiculovisita',
            name='vi_fecha_hora_salida',
            field=models.DateTimeField(blank=True, null=True, verbose_name='%Y-%m-%d %H:%M:%s'),
        ),
    ]
