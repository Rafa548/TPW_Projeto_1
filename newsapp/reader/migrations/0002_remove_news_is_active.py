# Generated by Django 4.0 on 2023-11-06 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='is_active',
        ),
    ]
