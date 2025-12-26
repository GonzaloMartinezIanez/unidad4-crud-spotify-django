from django.db import models

# Modelo de la tabla de usuarios
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)
    favourite_genre = models.CharField(max_length=100)
    # Tanto las canciones como los artistas se guardan en una lista en formato json
    # De esta forma no hay que crear otras tablas con claves externas
    songs = models.JSONField(default=list)
    artists = models.JSONField(default=list)

    def __str__(self):
        return self.username
