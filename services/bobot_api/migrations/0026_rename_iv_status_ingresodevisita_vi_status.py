# Generated by Django 4.2 on 2023-04-26 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0025_ingresodevisita_iv_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingresodevisita',
            old_name='iv_status',
            new_name='vi_status',
        ),
    ]
