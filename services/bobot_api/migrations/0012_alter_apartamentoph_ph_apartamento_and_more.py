# Generated by Django 4.2 on 2023-04-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0011_alter_apartamentosph_ph_apartamentocasa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartamentoph',
            name='ph_apartamento',
            field=models.PositiveSmallIntegerField(choices=[(101, 101), (102, 102), (103, 103), (104, 104), (1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AlterField(
            model_name='apartamentoph',
            name='ph_torre',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
        ),
    ]