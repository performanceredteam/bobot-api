# Generated by Django 4.2 on 2023-04-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0013_alter_apartamentoph_ph_torre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartamentoph',
            name='ph_apartamento',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='apartamentoph',
            name='ph_torre',
            field=models.PositiveIntegerField(),
        ),
    ]