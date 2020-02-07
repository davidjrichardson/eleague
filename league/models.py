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
    middle_names = models.CharField(max_length=128, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    experience = models.CharField(max_length=1, choices=EXPERIENCE)

    def __repr__(self):
        return f'<{self.first_name} {self.last_name}@{self.university} ({self.sex}/{self.experience}) created at {self.created_at}>'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['university', 'first_name', 'middle_names', 'last_name', 'sex', 'created_at'],
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
    num_arrows = models.PositiveIntegerField()

    @property
    def max_score(self):
        return (self.num_arrows * 10) if self.type == 'M' else (self.num_arrows * 9)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type', 'season'], name='unique_round')
        ]


class Division(models.Model):
    name = models.CharField(max_length=64)
    max_teams = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Division "{self.name}", max_teams: {self.max_teams}>'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(max_teams__gt=0), name='There must be at least 1 team per division')
        ]


class League(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    process_at = models.PositiveIntegerField()

    divisions = models.ManyToManyField(Division, related_name='divisions')

    class Meta:
        constraints = []


class LeagueEntry(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)

    score = models.PositiveIntegerField()
    hits = models.PositiveIntegerField()
    golds = models.PositiveIntegerField()
    xs = models.IntegerField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Update the edited_at field to reflect when it was updated
        self.edited_at = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['league', 'archer'], name='unique_archer_entry'),
        ]


class DivisionsField(models.TextField):
    """Deprecated but required for migrations"""
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
