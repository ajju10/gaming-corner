from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    discipline = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
