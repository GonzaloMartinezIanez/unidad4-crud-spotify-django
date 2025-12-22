from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    favourite_genre = models.CharField(max_length=100)
    songs = models.JSONField(default=list)
    artists = models.JSONField(default=list)

    def __str__(self):
        return self.username
