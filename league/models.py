from datetime import timedelta
from functools import reduce

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Round "{self.name}" type: {self.type}, season: {self.season}>'

    @property
    def max_score(self):
        return (self.num_arrows * 10) if self.type == 'M' else (self.num_arrows * 9)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type', 'season'], name='unique_round')
        ]


def non_zero_validator(value):
    if value == 0:
        raise ValidationError('Ensure this value is non-zero.'.format(value=value))


class Division(models.Model):
    name = models.CharField(max_length=64, help_text='The name of this division e.g.: "Division 1".')
    max_teams = models.IntegerField(default=-1,
                                    validators=[non_zero_validator, MinValueValidator(limit_value=-1)],
                                    help_text='The maximum number of teams from one university allowed into this division. Use -1 for unlimited teams.')

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<Division "{self.name}", max_teams: {self.max_teams}>'

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(max_teams=0), name='There must be at least 1 team per division')
        ]
        ordering = ('name',)


class LeagueSplit(models.Model):
    name = models.CharField(max_length=200, help_text='Then name of this split e.g.: "December/January".')
    split_starts = models.DateField(help_text='The first day for valid scores in this split. This date is inclusive.')
    split_ends = models.DateField(
        help_text='The last day that will be valid for scores in this split. This date is inclusive.')

    def __str__(self) -> str:
        return f'{self.name} ends {self.split_ends}'

    def __repr__(self) -> str:
        return f'<LeagueSplit "{self.name}", split ends: {self.split_ends}>'

    class Meta:
        ordering = ('split_ends', 'name')


class League(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    process_at = models.DurationField(default=timedelta(days=5),
                                      help_text='The amount of time after a split closes before the scores are processed and the league table(s) are generated for the split.')

    splits = models.ManyToManyField(LeagueSplit, related_name='splits')
    divisions = models.ManyToManyField(Division, related_name='divisions')

    def __str__(self) -> str:
        return f'{self.name} - {self.round}'

    class Meta:
        constraints = []


class LeagueEntryQuerySet(models.QuerySet):
    def for_league(self, league: League):
        return self.filter(league=league)

    def for_split(self, split: LeagueSplit):
        return self.filter(shot_at__gte=split.split_starts, shot_at__lt=split.split_ends)

    def for_club(self, university: ELeagueUser):
        return self.filter(archer__university=university)


class LeagueEntryManager(models.Manager):
    def get_queryset(self):
        return LeagueEntryQuerySet(self.model, using=self._db)

    def for_split(self, split: LeagueSplit) -> LeagueEntryQuerySet:
        return self.get_queryset().for_split(split)

    def for_club(self, university: ELeagueUser) -> LeagueEntryQuerySet:
        return self.get_queryset().for_club(university)

    def for_league(self, league: League) -> LeagueEntryQuerySet:
        return self.get_queryset().for_league(league)


class LeagueEntry(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    archer = models.ForeignKey(Archer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(null=True, blank=True)
    shot_at = models.DateTimeField()

    score = models.PositiveIntegerField()
    hits = models.PositiveIntegerField()
    golds = models.PositiveIntegerField()
    xs = models.IntegerField(blank=True, null=True)

    objects = LeagueEntryManager()

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
