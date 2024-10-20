# Generated by Django 5.0.7 on 2024-08-13 14:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siedlungsmanager', '0008_objekt_aktuelle_miete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siedlung',
            name='baurechtszins',
            field=models.PositiveIntegerField(blank=True, help_text='Baurechtszins falls vorhanden', null=True, verbose_name='Baurechtszins'),
        ),
        migrations.AlterField(
            model_name='siedlung',
            name='betriebsquote_zuschlag',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Wert wischen 0 und 100 mit maximal zwei Nachkommastellen', max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Betriebsquote Zuschlag'),
        ),
    ]
