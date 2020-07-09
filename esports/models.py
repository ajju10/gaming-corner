from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.datetime_safe import datetime

User = settings.AUTH_USER_MODEL


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    discipline = models.CharField(max_length=100)
    is_team = models.BooleanField(default=False)
    size = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_ongoing_tournaments():
        return Tournament.objects.filter(start_time__lt=datetime.now(), end_time__gt=datetime.now())

    @staticmethod
    def get_planned_tournaments():
        return Tournament.objects.filter(start_time__gt=datetime.now())


class Team(models.Model):
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name


class Participant(models.Model):
    email = models.EmailField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @staticmethod
    def team_players():
        return Participant.objects.filter(team__isnull=False)

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.name
