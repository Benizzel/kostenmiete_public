# Generated by Django 5.0.7 on 2024-08-25 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siedlungsmanager', '0012_alter_siedlung_betriebsquote_zuschlag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objekt',
            options={'ordering': ['internal_oid'], 'verbose_name': 'Objekt', 'verbose_name_plural': 'Objekte'},
        ),
        migrations.AlterModelOptions(
            name='siedlung',
            options={'ordering': ['internal_id'], 'verbose_name': 'Siedlung', 'verbose_name_plural': 'Siedlungen'},
        ),
    ]
