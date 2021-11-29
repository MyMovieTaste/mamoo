from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.conf import settings

# Create your models here.

class Year(models.Model):
    """영화 개봉년도 클래스"""
    id = models.CharField(primary_key=True, max_length=4)

class Bookmark(models.Model):
    """북마크 클래스"""
    pass

class Genre(models.Model):
    """장르 클래스"""
    name = models.TextField()

    def __str__(self):
        return self.name
    
class Movie(models.Model):
    """영화 클래스"""
    title = CharField(max_length=100)
    overview = TextField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    release_date = models.DateField()
    poster_path = models.CharField(max_length=200)
    ranking = models.IntegerField()
    # 1:N
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True)
    # M:N
    genre_ids = models.ManyToManyField(Genre, related_name='movie_genre')  
    # 이 영화를 북마크 한 사람
    bookmarked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bookmarked_movies")

    def __str__(self):
        return self.title

    
class Review(models.Model):
    """리뷰 클래스"""
    content = models.TextField()
    rank = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 1:N
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_reviews', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 대댓글
    # parent_review = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.movie_title