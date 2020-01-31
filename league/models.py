import re

from functools import reduce

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from dashboard.models import ELeagueUser


class Archer(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    EXPERIENCE = (
        ('N', 'Novice'),
        ('E', 'Experienced'),
    )

    # TODO: Figure out how deleting user data should work?
    university = models.ForeignKey(ELeagueUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    created_at = models.DateTimeField(default=timezone.now)

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    experience = models.CharField(max_length=1, choices=EXPERIENCE)

    def __repr__(self):
        return f'<{self.first_name} {self.last_name}@{self.university} ({self.sex}/{self.experience}) created at {self.created_at}>'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'first_name', 'last_name', 'sex', 'created_at'],
                                    name='unique_archer')
        ]


class Round(models.Model):
    SCORING_TYPE = (
        ('M', 'Metric'),
        ('I', 'Imperial'),
    )

    SEASONS = (
        ('I', 'Indoor'),
        ('O', 'Outdoor')
    )

    name = models.CharField(max_length=64)
    description = models.TextField()

    type = models.CharField(max_length=1, choices=SCORING_TYPE)
    season = models.CharField(max_length=1, choices=SEASONS)
    num_arrows = models.IntegerField()

    @property
    def max_score(self):
        return (self.num_arrows * 10) if self.type == 'M' else (self.num_arrows * 9)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type', 'season'], name='unique_round')
        ]


class Division:
    def __init__(self, name, max_teams):
        self.name = name
        self.max_teams = max_teams

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Division "{self.name}", max_teams: {self.max_teams}>'

    @staticmethod
    def parse_division(division_string):
        # Division is made up of a tuple: (name,max_teams) - names may contain alphanumeric chars and whitespace
        parse_regex = re.compile(r'\((?P<name>[\w ]+),(?P<num>\d+)\)')
        match = parse_regex.match(division_string)

        # Catch if it cannot parse the division tuple
        if not match:
            raise ValidationError(f'Failed to parse {division_string} as Division object')

        if not match.groupdict().get('name') or not match.groupdict().get('num'):
            raise ValidationError(f'Failed to parse {division_string} as Division object')

        return Division(name=match.groupdict().get('name'), max_teams=match.groupdict().get('num'))

    def serialise(self):
        return f'({self.name},{self.max_teams})'


class DivisionsField(models.TextField):
    description = 'A league divison'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        return super().deconstruct()

    def from_db_value(self, value, expression, connection):
        # This field will contain multiple divisions: (div),(div),(div)
        if value is None:
            return value

        divisions_raw = value.split(';')
        return list(map(lambda d: Division.parse_division(d), divisions_raw))

    def to_python(self, value):
        if isinstance(value, list):
            # Check that the list is of one type
            is_monomorphic = reduce(lambda x, y: x and y,
                                    map(lambda i: isinstance(i, Division), value))
            if is_monomorphic:
                return value
            else:
                raise ValidationError('Cannot parse list; some items are not Divisions')

        if value is None:
            return value

        divisions_raw = value.split(';')
        return list(map(lambda d: Division.parse_division(d), divisions_raw))

    def get_prep_value(self, value):
        return '[' + ';'.join(map(lambda d: d.serialise(), value)) + ']'

    # TODO: Override the form field


class League(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    divisions = DivisionsField()

    class Meta:
        constraints = []


class LeagueEntry(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)

    score = models.IntegerField()
    hits = models.IntegerField()
    golds = models.IntegerField()
    xs = models.IntegerField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Update the edited_at field to reflect when it was updated
        self.edited_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['league', 'archer'], name='unique_archer_entry'),
            models.CheckConstraint(check=models.Q(score__gte=0), name='score_positive'),
            models.CheckConstraint(check=models.Q(hits__gte=0), name='hits_positive'),
            models.CheckConstraint(check=models.Q(golds__gte=0), name='golds_positive'),
        ]
