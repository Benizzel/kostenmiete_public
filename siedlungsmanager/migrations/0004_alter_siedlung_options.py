# Generated by Django 5.0.7 on 2024-08-09 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siedlungsmanager', '0003_alter_siedlung_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='siedlung',
            options={'ordering': ['internal_id']},
        ),
    ]
