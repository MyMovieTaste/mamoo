from rest_framework import serializers
from .models import Genre, Movie, Review


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('review', )

# class CommentListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user')

# class ReviewListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True, read_only=True) # 영화에 달린 모든 댓글
    class Meta:
        model = Movie
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    review_count = serializers.IntegerField(source='review_set.count', read_only=True) # 영화에 달린 모든 리뷰수
    class Meta:
        model = Movie
        fields = '__all__'

# SerializerMethodField 사용하여 필드추가
# 해당 오브젝트(쿼리셋)에 .values()를 붙이고 리스트로 감싸자!
class RecentMovieByGenreListSerializer(serializers.ModelSerializer):
    movies_by_genre = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'

    def get_movies_by_genre(self, obj):
        movies = Movie.objects.all().order_by('-release_date')
        genre_ids = Genre.objects.all().values('id').values()

        movies_by_genre = []
        for genre_id in genre_ids: 
            movies_by_genre.append(movies.filter(genre_ids=genre_id['id']).values())
        
        return movies_by_genre

class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class RecommendMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'



