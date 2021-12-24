from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Movie, Genre, Review, Year
from .serializers import MovieSearchSerializer, MovieListSerializer, MovieSerializer, ReviewListSerializer, BestVoteMovieByYearListSerializer, RecommendMovieSerializer, ReviewSerializer, RecentMovieByGenreListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from collections import Counter
from itertools import islice
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.http.response import JsonResponse

#=> year.json 파일로 대체
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def create_year_table(request):
#     """연도테이블을 생성하는 함수"""
#     batch_size = 10
#     objs = (Year(id=year) for year in range(1950, 2022))
#     while True:
#         batch = list(islice(objs, batch_size))
#         if not batch:
#             break
#         Year.objects.bulk_create(batch, batch_size)

# 지우고싶은 특정 테이블(Review) 삭제
@api_view(['GET'])
@permission_classes([AllowAny])
def delete_table(request):
    Review.objects.all().delete()
    context= {}
    return context




@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    """영화를 제목으로 검색하는 함수"""
    print('request.GET:' ,request.GET)
    keyword = request.GET['keyword']
    result = Movie.objects.filter(title__contains=keyword)
    serializer = MovieSearchSerializer(result, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny]) 
def movie_list(request):
    """영화리스트 정보를 반환하는 함수"""
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny]) 
def recent_movie_by_genre(request):
    """장르별 최신 개봉 영화"""
    genres = Genre.objects.all()
    serializer = RecentMovieByGenreListSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny]) 
def best_vote_movie_by_year(request):
    """연도별 평균 별점순 영화"""
    # years = get_list_or_404(Year) # order_by 사용불가
    years = Year.objects.all().order_by('-id')
    serializer = BestVoteMovieByYearListSerializer(years, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_details(request, movie_pk):
    """영화 상세 정보"""
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializers = MovieSerializer(movie)
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_recommend(request):
    """영화 추천"""
    user = request.user
    user = getattr(user, 'id')
    user_reviews = Review.objects.all().filter(user=user)
    
    # (추가할부분 : 유저가 영화에 리뷰를 4점 줬다가 2점 주면, 해당 리뷰평점은 2점인것으로 가정)

    review_gte4 = user_reviews.filter(rank__gte=4)
    review_gte4_count = user_reviews.filter(rank__gte=4).count()

    # 1. 리뷰수 5개 이상이면 4점 이상 준 영화 담는다. 
    if review_gte4_count >= 5:
        movie_list_gte4 = []
        for review in review_gte4:
            movie_id = getattr(review, 'movie_id') # 13  # object의 value는 getattr로 얻는다.
            # 중복되는 리뷰는 처음것만 담는다.
            if movie_id not in movie_list_gte4:
                movie_list_gte4.append(movie_id)   
        
        # 2. 유저가 남긴 리뷰를 제외한 리뷰들 중 같은 영화의 리뷰를 남긴 유저들을 찾는다.
        reviews = Review.objects.all().exclude(user=user)
        #<QuerySet [<Review: 121>, <Review: 278>, <Review: 857>, <Review: 14>, <Review: 14>, <Review: 14>, <Review: 76>, <Review: 70>, <Review: 24>, <Review: 13>]>
        # reviews = Review.objects.all().exclude(user=request.user)
        same_taste_users = []
        #print(movie_list_gte4) # [13, 24, 122, 335, 598, 1124, 4348, 489, 14]
        for movie in movie_list_gte4:
            for review in reviews:
                user_id = getattr(review, 'user_id')
                movie_id = getattr(review, 'movie_id')
                if movie_id == movie and user_id not in same_taste_users: # 겹치는 유저 제거
                    same_taste_users.append(user_id)
        #print(same_taste_users) # [6]

        # 3. 비슷한 취향 유저의 리뷰리스트에서 높은 평점 중 내가 쓴 리뷰의 영화와 겹치지 않는 영화를 추천한다.
        recommend_movies = []
        User = get_user_model()
        for same_taste_user in same_taste_users:
            s = User.objects.get(id=same_taste_user) 
            reviews = s.user_reviews.all() # 해당 유저가 쓴 모든 리뷰
            rm = reviews.filter(user=same_taste_user).values('movie') # QuerySet [{'movie': 121}, {'movie': 278}, 

            for r in rm:
                if r['movie'] not in movie_list_gte4:  # 121, 278, 857, 14, 14, 14,...
                    recommend_movies.append(r['movie'])

        recommend_movies_no_overlap_ids = list(set(recommend_movies)) # 중복제거 # [121, 278, 857, 76, 70]

        # 최대 12개 출력
        recommend_movies_no_overlap = Movie.objects.filter(id__in=recommend_movies_no_overlap_ids)[:12] # Movie QuerySet

        # 4. 만약 추천 갯수가 5개 미만이면, 인기도 순(popularity), 최신순으로 5개를 더 출력한다. (front)

        serializers = RecommendMovieSerializer(recommend_movies_no_overlap, many=True)
        return Response(serializers.data)

# => 장르비율: 미사용상태
# @api_view(['GET'])
# # 특정 사용자가 4점이상 준 리뷰들의 장르별 비율을 구한다.
# def movie_mypick_genre_ratio(request):
#     # token 받기 전 
#     # user_pk = request.data['user'] # 5
#     # User = get_user_model()
#     # user = get_object_or_404(User, pk=user_pk) # test1
#     # token 받은 후
#     user = request.user
#     user_reviews = Review.objects.all().filter(user=user)

#     review_gte4 = user_reviews.filter(rank__gte=4)
#     review_gte4_count = user_reviews.filter(rank__gte=4).count()

#     # 1. 4점 이상인 리뷰를 골라서 해당 영화 정보를 찾는다.
#     if review_gte4_count >= 5:
#         movie_list_gte4 = []
#         for review in review_gte4:
#             movie_id = getattr(review, 'movie_id') 
#             if movie_id not in movie_list_gte4:
#                 movie_list_gte4.append(movie_id)   

#     # 2. 해당 영화들의 장르를 담는다. (중복포함)
#     genres_movie_list_gte4 = [] # [13, 24, 122, 335, 598, 1124, 4348, 489, 14]
#     for movie_id in movie_list_gte4:
#         movie = Movie.objects.filter(id=movie_id) 
#         genre_ids = movie.values('genre_ids') # [{'genre_ids': 18}, {'genre_ids': 35}, {'genre_ids': 10749}]>
        
#         for genre_id in genre_ids:
#                 genres_movie_list_gte4.append(genre_id['genre_ids'])

#     # 3. 장르별 갯수를 구한다.  => 변경 | 장르별 비율만 front로 전달
#     genre_ratio_movie_list_gte4 = dict(Counter(genres_movie_list_gte4)) 

#     total = sum(genre_ratio_movie_list_gte4.values())

#     for genre_id, cnt in genre_ratio_movie_list_gte4.items():
#         genre_ratio_movie_list_gte4[genre_id] = round(cnt / total * 100, 1)
        
#     return Response(genre_ratio_movie_list_gte4)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmarks(request, movie_pk):
    """북마크 기능"""
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if user not in movie.bookmarked_users.all():
        user.bookmarked_movies.add(movie)
    else:
        user.bookmarked_movies.remove(movie)

    data = {
        'message' : 'bookmarked!'
    }
    
    return JsonResponse(data=data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_list_or_create(request, movie_pk):
    """리뷰 리스트 가져오기 및 (특정 영화의)리뷰 작성하기"""

    if request.method == 'GET':
        reviews = Review.objects.all()
        movie_reviews = reviews.filter(movie=movie_pk).order_by("created_at")
        serializer = ReviewListSerializer(movie_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method =='POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review_detail_or_update_or_delete(request, review_pk):
    """특정 영화의 리뷰 자세히보기, 수정 및 삭제하기"""

    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # 본인 게시글만 수정가능
        # if not request.user.review_set.filter(pk=review_pk).exists():
        #     return Response({'detail' : '권한이 없습니다.'}, status=HTTP_403_FORBIDDON)

        user = request.user
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'DELETE':
        review.delete()
        data = {
            'message' : 'deleted',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)   