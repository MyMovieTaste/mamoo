from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Movie, Genre, Review
from .serializers import MovieListSerializer, MovieSerializer, RecommendMovieSerializer, GenreListSerializer, ReviewSerializer, RecentMovieByGenreListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404, render
from collections import Counter

# 영화 리스트
@api_view(['GET'])
@permission_classes([AllowAny]) # 테스트 시에만 사용
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 최신 개봉일 순 > 장르별 (장르별 최신 개봉영화)
@api_view(['GET'])
@permission_classes([AllowAny]) 
def recent_movie_by_genre_list(request):
    genres = Genre.objects.all()
    serializer = RecentMovieByGenreListSerializer(genres, many=True)
    return Response(serializer.data)

# 평균 별점 높은 순 > 연도별 (연도별 평균 별점 순위)
@api_view(['GET'])
@permission_classes([AllowAny]) 
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 상세정보
@api_view(['GET'])
@permission_classes([AllowAny])
def get_details(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializers = MovieSerializer(movie)
    return Response(serializers.data)

# 영화 추천
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_recommend(request):
    user_reviews = Review.objects.all().filter(user=request.user)
    review_gte4 = user_reviews.filter(rank__gte=4)
    review_gte4_count = user_reviews.filter(rank__gte=4).count()

    if review_gte4_count >= 5:
        movie_list_gte4 = []
        for review in review_gte4:
            movie_list_gte4.append(review.movie) 

        reviews = Review.objects.all().exclude(user=request.user)
        same_taste_users = []
        for movie in movie_list_gte4:
            for review in reviews:
                if review.movie == movie:
                    same_taste_users.append(review.user)
        
        recommend_movies = []
        for same_taste_user in same_taste_users:
            recommend_movie = reviews.filter(user=same_taste_user).values('movie_ids')
            if recommend_movie not in movie_list_gte4:
                recommend_movies.append(recommend_movie)
        recommend_movies_no_overlap = list(set(recommend_movies)) # 중복제거
        
        serializers = RecommendMovieSerializer(recommend_movies_no_overlap, many=True)
        return Response(serializers.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_recommend_genre(request):
    # 장르 제외한 추천과 동일한 부분
    user_reviews = Review.objects.all().filter(user=request.user)
    review_gte4 = user_reviews.filter(rank__gte=4)
    review_gte4_count = user_reviews.filter(rank__gte=4).count()

    if review_gte4_count >= 5:
        movie_list_gte4 = []
        for review in review_gte4:
            movie_list_gte4.append(review.movie) 

        reviews = Review.objects.all().exclude(user=request.user)
        same_taste_users = []
        for movie in movie_list_gte4:
            for review in reviews:
                if review.movie == movie:
                    same_taste_users.append(review.user)
        
        recommend_movies = []
        for same_taste_user in same_taste_users:
            recommend_movie = reviews.filter(user=same_taste_user).values('movie_ids')
            if recommend_movie not in movie_list_gte4:
                recommend_movies.append(recommend_movie)

    #장르추가########################################################

    genres_movie_list_gte4 = [] # [12, 28, 878]
    for movie_id in movie_list_gte4:
        movie = Movie.objects.all().filter(id=movie_id)
        genre_ids = movie.values('genre_ids')
        # <QuerySet [{'genre_ids': 12}, {'genre_ids': 28}, {'genre_ids': 878}]>
        for genre_id in genre_ids:
                genres_movie_list_gte4.append(genre_id['genre_ids'])

    genre_ratio_movie_list_gte4 = dict(Counter(genres_movie_list_gte4)) # {12: 1, 28: 1, 878:1}

    result = []
    for genre_id, cnt in genre_ratio_movie_list_gte4.items(): # 12,1  28,1  878,1
        c = 0
        for i in range(len(recommend_movies)):
            movie = Movie.objects.get(id=recommend_movies[i])
            if genre_id in movie.genre_ids:
                result.append(movie)
                recommend_movies.pop(i)
                c += 1
                if c == cnt:
                    break
            else:
                # 동일 장르이면서 평점(vote_average)가 높은 영화
                alt = Movie.objects.filter(genre_ids__contains=genre_id).order_by('-vote_average')
                result.append(alt)
                c += 1
                if c == cnt:
                    break

    serializers = RecommendMovieSerializer(result, many=True)
    return Response(serializers.data)


# 장르 리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def genre_list(request):
    genrelist = list(Genre.objects.all())
    serializers = GenreListSerializer(genrelist, many=True)
    return Response(serializers.data)


# 리뷰리스트 및 리뷰작성(특정 영화의)
@api_view(['GET', 'POST' , 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_list_or_create(request, movie_pk):

    if request.method == 'GET':
        reviews = Review.objects.all()
        movie_reviews = reviews.filter(movie=movie_pk).order_by("created_at")
        serializer = ReviewSerializer(movie_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method =='POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # elif request.method == 'PUT':
    #     movie = get_object_or_404(Movie, pk=movie_pk)
    #     serializer = ReviewSerializer(movie, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save(movie=movie)
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    # elif request.method == 'DELETE':
    #     movie.review.delete()
    #     data = {
    #         'message' : 'deleted',
    #     }
    #     return Response(data, status=status.HTTP_204_NO_CONTENT)   


# # 댓글리스트 및 댓글작성
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def comment_list_or_create(request, review_pk):

#     if request.method == 'GET':
#         comments = get_object_or_404(Comment)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method =='POST':
#         review = get_object_or_404(Review, pk=review_pk)
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(review=review)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# # 개별 댓글 보기 수정 삭제
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([AllowAny])
# def comment_detail_or_update_or_delete(request, review_pk):
#     review = get_object_or_404(Comment, pk=review_pk)
#     if request.method == 'GET':
#         serializer = CommentSerializer(review)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         serializer = CommentSerializer(review, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(review=review)
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
#     elif request.method == 'DELETE':
#         review.comment.delete()
#         data = {
#             'message' : 'deleted',
#         }
#         return Response(data, status=status.HTTP_204_NO_CONTENT)