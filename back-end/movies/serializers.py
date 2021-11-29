from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Genre, Movie, Review, Year
from django.contrib.auth import get_user_model

class ReviewListSerializer(serializers.ModelSerializer):
    """개별 영화의 리뷰리스트 보기"""
    user = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user',)

class ReviewSerializer(serializers.ModelSerializer):
    """개별 영화의 개별 리뷰 상세보기"""
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user',)

class MovieSearchSerializer(serializers.ModelSerializer):
    """영화 검색"""
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    """영화 상세정보"""
    review_set = ReviewSerializer(many=True, read_only=True) # 영화에 달린 모든 댓글
    class Meta:
        model = Movie
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    """영화 리스트"""
    review_count = serializers.IntegerField(source='review_set.count', read_only=True) # 영화에 달린 모든 리뷰수
    class Meta:
        model = Movie
        fields = '__all__'

class RecentMovieByGenreListSerializer(serializers.ModelSerializer):
    """장르별 개봉순 영화"""
    movies_by_genre = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'name', 'movies_by_genre',)

    def get_movies_by_genre(self, obj):
        
        movies = Movie.objects.all().order_by('-release_date')
        movies = movies.filter(genre_ids=obj.id)
        return MovieListSerializer(movies, many=True).data 
        # return movies.filter(genre_ids=obj.id).values() => M:N(bookmarked_user) 이 출력되지 않음.

class BestVoteMovieByYearListSerializer(serializers.ModelSerializer):
    """연도별 평균별점순 영화"""
    movies_by_year = serializers.SerializerMethodField()

    class Meta:
        model = Year
        fields = ('id','movies_by_year',)

    def get_movies_by_year(self, obj):

        movies = Movie.objects.all().order_by('-vote_average')
        movies = movies.filter(year_id=obj.id)
        return MovieListSerializer(movies, many=True).data
        # return movies.filter(year_id=obj.id).values() => M:N(bookmarked_user) 이 출력되지 않음.

class RecommendMovieSerializer(serializers.ModelSerializer):
    """영화추천"""
    class Meta:
        model = Movie
        fields = '__all__'
