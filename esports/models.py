from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    discipline = models.CharField(max_length=100)
    is_team = models.BooleanField(default=False)
    size = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
