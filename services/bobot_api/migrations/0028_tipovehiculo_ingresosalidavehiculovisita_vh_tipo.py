# Generated by Django 4.2 on 2023-05-01 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0027_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('vh_tipo', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('vh_desc', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='ingresosalidavehiculovisita',
            name='vh_tipo',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='bobot_api.tipovehiculo'),
            preserve_default=False,
        ),
    ]
