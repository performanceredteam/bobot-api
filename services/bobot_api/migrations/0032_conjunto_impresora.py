# Generated by Django 4.2 on 2024-05-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bobot_api', '0031_alter_facturacion_fa_tiempo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conjunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cj_nombre', models.CharField(max_length=50)),
                ('cj_direccion', models.CharField(max_length=50)),
                ('cj_ciudad', models.CharField(max_length=50)),
                ('cj_tek', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Impresora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cg_impresora', models.BooleanField()),
            ],
        ),
    ]