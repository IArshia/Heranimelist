from typing import Any
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Anime(models.Model):
    name = models.CharField(max_length=255)
    summery = models.TextField(blank=True)
    myanimelist_score = models.DecimalField(max_digits=6, decimal_places=2)
    released_date = models.DateField()
    image_url = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name
    


class Score(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='scores')
    user_score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    


class ListAnime(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ListAnimeItem(models.Model):
    list = models.ForeignKey(ListAnime, on_delete=models.CASCADE, related_name='items')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['list', 'anime']]


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=1023)

    def __str__(self) -> str:
        return self.user.username
    






