from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie, Genre, Review, Comment
from .serializers import MovieListSerializer, MovieDetailSerializer, GenreRecommendListSerializer, GenreListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404, render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import requests
import random
from .serializers import ReviewSerializer, CommentSerializer


# 영화 리스트
@api_view(['GET'])
@permission_classes([AllowAny]) # 테스트 시에만 사용
def top_rated_movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 상세정보
@api_view(['GET'])
@permission_classes([AllowAny])
def get_details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    serializers = MovieDetailSerializer(movie)
    return Response(serializers.data)

# 장르 추천
@api_view(['GET'])
@permission_classes([AllowAny])
def genre_recommend(request):
    genrelist = list(Genre.objects.all())
    recommend_list = []
    for genre in genrelist:
        genre_movies = genre.movie_genre.all() # 장르별 영화들
        if genre_movies:
            movie = random.choice(genre_movies)
            if movie not in recommend_list:
                recommend_list.append((genre, movie))
    recommend_list = random.sample(set(recommend_list), 10)
    # context = {
    # 'recommend_list': recommend_list,
    # }   
    # return render(request, 'movies/recommend.html', context)
    serializers = GenreRecommendListSerializer(recommend_list, many=True)
    return Response(serializers.data)

# 장르 리스트
@api_view(['GET'])
@permission_classes([AllowAny])
def genre_list(request):
    genrelist = list(Genre.objects.all())
    serializers = GenreListSerializer(genrelist, many=True)
    return Response(serializers.data)


 # 리뷰: 보기 쓰기 업데이트 삭제
    path('reviews/', views.review_list_or_create), # get, post
    path('reviews/<int:review_pk>/', views.review_detail_or_update_or_delete), # get, post, put, delete

    # 리뷰 댓글: 보기 쓰기 삭제
    path('reviews/<int:review_pk>/comments/', views.comment_list_or_create), # get, post
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.review_detail_or_delete) # get, post, put, delete

# 리뷰리스트 및 리뷰 작성
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_list_or_create(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Review)
        serializers = ReviewSerializer(reviews, many=True)
        return Response(serializers.data)

    elif request.method =='POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


# 개별 리뷰 보기 수정 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_detail_or_update_or_delete(request, pk):
    review = get_list_or_404(Review, pk=pk)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        review.delete()
        data = {
            'message' : 'deleted',
        }
        return Response(data)

    
# 댓글 작성하기
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comment_list_or_create(request):
    reviews = get_list_or_404(Review)
    serializers = ReviewSerializer(reviews, many=True)
    return Response(serializers.data)



