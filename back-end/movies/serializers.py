from rest_framework import serializers
from .models import Genre, Movie, Review

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class GenreRecommendListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'



