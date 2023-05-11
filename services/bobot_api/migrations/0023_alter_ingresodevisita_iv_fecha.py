# Generated by Django 4.2 on 2023-04-26 19:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0022_alter_ingresodevisita_iv_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresodevisita',
            name='iv_fecha',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='%Y-%m-%d %H:%M:%s'),
        ),
    ]