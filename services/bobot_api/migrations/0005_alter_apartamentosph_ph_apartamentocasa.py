# Generated by Django 4.2 on 2023-04-23 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0004_alter_apartamentoph_ph_apartamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartamentosph',
            name='ph_apartamentocasa',
            field=models.PositiveBigIntegerField(verbose_name='AptoCasa'),
        ),
    ]
