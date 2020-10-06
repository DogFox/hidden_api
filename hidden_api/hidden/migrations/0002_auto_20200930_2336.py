# Generated by Django 2.1.15 on 2020-09-30 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hidden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretboxmembers',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='friend', to='hidden.User'),
        ),
        migrations.AlterField(
            model_name='secretboxmembers',
            name='secretbox',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='secretbox', to='hidden.SecretBox'),
        ),
        migrations.AlterField(
            model_name='secretboxmembers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='hidden.User'),
        ),
    ]