from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.conf import settings

# Create your models here.


class Bookmark(models.Model):
    pass

class Genre(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = CharField(max_length=100)
    overview = TextField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    release_date = DateTimeField()
    poster_path = models.CharField(max_length=200)
    ranking = models.IntegerField()
    # M:N
    genre_ids = models.ManyToManyField(Genre, related_name='movie_genre')
    # 이 영화를 북마크 한 사람
    bookmarked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bookmarked_movies")

    def __str__(self):
        return self.title

    
class Review(models.Model):
    movie_title = models.CharField(max_length=100)
    content = models.TextField()
    RATINGS = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rank = models.IntegerField(choices=RATINGS, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 1:N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 대댓글
    # parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.movie_title

# class Comment(models.Model):
#     content = models.TextField()
#     # 1:N
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title
