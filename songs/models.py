from django.db import models

# Create your models here.

class Song(models.Model):
    track_id = models.CharField(max_length=100)
    track = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    votes = models.IntegerField(default=1)
    def __str__(self):
        return self.track