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
