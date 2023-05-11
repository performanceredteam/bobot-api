# Generated by Django 4.2 on 2023-04-23 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0002_torresph_alter_apartamentoph_ph_torre'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartamentosPh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_apartamentocasa', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='torresph',
            name='tr_torre',
            field=models.PositiveSmallIntegerField(verbose_name='Torre'),
        ),
        migrations.AlterField(
            model_name='apartamentoph',
            name='ph_apartamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bobot_api.apartamentosph'),
        ),
    ]
