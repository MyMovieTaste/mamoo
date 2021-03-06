from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie

class UserSerializer(serializers.ModelSerializer):
    """회원가입"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)

class MovieSerializer(serializers.ModelSerializer):
    """영화 정보"""
    class Meta:
        model = Movie
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """프로필 정보"""
    bookmarked_movies = MovieSerializer(many=True) 
    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True) 
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'followings_count','followings','followers_count', 'followers','bookmarked_movies', 'id')

