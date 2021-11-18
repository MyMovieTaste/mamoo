from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.TextField()

class Movie(models.Model):
    title = CharField(max_length=100)
    overview = TextField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    release_date = DateTimeField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genre_ids = models.ManyToManyField(Genre, related_name='movie_genre')

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    RANKS = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rank = models.IntegerField(choices=RANKS, default=5)

    def __str__(self):
        return self.title


# class Rating(models.Model):
#     # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     # rates = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
#     def __str__(self):
#         return self.title