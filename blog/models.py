from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
