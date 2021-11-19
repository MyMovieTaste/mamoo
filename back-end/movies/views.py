from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .get_movie_data import tmdb
import requests

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny]) # 테스트 시에만 사용
def top_rated_movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

### detail
@api_view(['GET'])
@permission_classes([AllowAny])
def get_details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    serializers = MovieDetailSerializer(movie)
    return Response(serializers.data)