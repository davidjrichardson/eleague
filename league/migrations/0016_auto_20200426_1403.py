# Generated by Django 3.0.1 on 2020-04-26 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0015_league_splits'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='division',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='leaguesplit',
            options={'ordering': ('split_ends', 'name')},
        ),
        migrations.AddField(
            model_name='leaguesplit',
            name='split_starts',
            field=models.DateField(default=django.utils.timezone.now, help_text='The first day for valid scores in this split. This date is inclusive.'),
            preserve_default=False,
        ),
    ]
