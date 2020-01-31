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
        return (self.num_arrows * 10) if self.type is 'M' else (self.num_arrows * 9)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type', 'season'], name='unique_round')
        ]
