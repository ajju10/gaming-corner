# Generated by Django 3.0.7 on 2020-07-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esports', '0004_auto_20200728_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]