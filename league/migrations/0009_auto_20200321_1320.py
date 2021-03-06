# Generated by Django 3.0.1 on 2020-03-21 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_league_splits'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='division',
            name='There must be at least 1 team per division',
        ),
        migrations.AlterField(
            model_name='division',
            name='max_teams',
            field=models.IntegerField(default=-1, help_text='The maximum number of teams from one university allowed into this division. Use -1 for unlimited teams.'),
        ),
        migrations.AddConstraint(
            model_name='division',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, max_teams=0), name='There must be at least 1 team per division'),
        ),
    ]
