from django.contrib.auth.models import User
from django.db import models


class ELeagueUser(models.Model):
    """
    This class represents a user that signs into the website to submit scores. It is not associated with any score.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    university = models.TextField(unique=True)  # Only one user can be tied to a university

    def __str__(self):
        return self.university
