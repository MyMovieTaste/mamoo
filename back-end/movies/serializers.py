from rest_framework import serializers
from .models import Genre, Movie, Review, Year
from django.contrib.auth import get_user_model



# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('review', )

# class CommentListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'

# 리뷰 불러오기 및 작성
class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user',)

# 리뷰 상세
# NestSerialiser -> StringRelatedField 
# class UsernameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('id', 'username',)
        
class ReviewSerializer(serializers.ModelSerializer):
    # user = UsernameSerializer(read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user',)

# 영화검색
class MovieSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# 영화 상세
class MovieSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=True) # 영화에 달린 모든 댓글
    class Meta:
        model = Movie
        fields = '__all__'

# 영화 리스트
class MovieListSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(source='review_set.count', read_only=True) # 영화에 달린 모든 리뷰수
    class Meta:
        model = Movie
        fields = '__all__'

# 장르별 개봉순 영화
class RecentMovieByGenreListSerializer(serializers.ModelSerializer):
    movies_by_genre = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'movies_by_genre']

    def get_movies_by_genre(self, obj):
        movies = Movie.objects.all().order_by('-release_date')
        return movies.filter(genre_ids=obj.id).values() # 입력받은 아이디와 일치여부 확인,.values()를 붙여야

# 연도별 평균별점순 영화
class BestVoteMovieByYearListSerializer(serializers.ModelSerializer):
    movies_by_year = serializers.SerializerMethodField()

    class Meta:
        model = Year
        fields = ['id','movies_by_year']

    def get_movies_by_year(self, obj):
        movies = Movie.objects.all().order_by('-vote_average')
        return movies.filter(year_id=obj.id).values()


# 장르 리스트
class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

# 영화추천
class RecommendMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'