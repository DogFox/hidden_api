# Generated by Django 2.1.15 on 2020-10-01 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hidden', '0004_auto_20201001_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secretboxmembers',
            name='friend',
        ),
    ]
