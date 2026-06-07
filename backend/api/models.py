from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    display_name = models.CharField(max_length=50, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.display_name if self.display_name else self.user.username
