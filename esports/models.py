from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.datetime_safe import datetime

User = settings.AUTH_USER_MODEL


class CannotParticipateException(Exception):
    pass


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discipline = models.CharField(max_length=100)
    is_team = models.BooleanField(default=False)
    size = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    start_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.name}: {self.discipline}"

    def remaining_slots(self):
        return self.size - self.participant.count()

    @staticmethod
    def get_ongoing_tournaments():
        return Tournament.objects.filter(start_time__lt=datetime.now(), end_time__lte=datetime.now())

    @staticmethod
    def get_planned_tournaments():
        return Tournament.objects.filter(end_time__gt=datetime.now())

    @staticmethod
    def past_tournaments():
        return Tournament.objects.filter(Q(start_time__lt=datetime.now()) & Q(end_time__lt=datetime.now()))

    def is_full(self):
        count = Participant.objects.filter(tournament_id=self.id).count()
        size = self.size
        if size <= count:
            return True
        return False


class Participant(models.Model):
    email = models.EmailField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participant')
    name = models.CharField(max_length=250, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.email

    def __str__(self):
        return f"{self.email}: {self.tournament}"
    
    def save(self, *args, **kwargs):
        if self.tournament.is_full():
            raise CannotParticipateException("Tournament is already full. Please join other tournaments.")
        elif self.tournament.end_time < datetime.now():
            raise CannotParticipateException("Tournament registration has been closed.")
        super(Participant, self).save(*args, **kwargs)
