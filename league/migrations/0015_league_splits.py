# Generated by Django 3.0.1 on 2020-03-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0014_auto_20200321_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='splits',
            field=models.ManyToManyField(related_name='splits', to='league.LeagueSplit'),
        ),
    ]
