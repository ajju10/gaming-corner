# Generated by Django 3.0.7 on 2020-06-12 15:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esports', '0004_tournament_discipline'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_team',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tournament',
            name='organizer',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='size',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
    ]