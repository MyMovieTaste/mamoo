from django.contrib import admin
from .models import Movie, Review, Bookmark, Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(Genre)
