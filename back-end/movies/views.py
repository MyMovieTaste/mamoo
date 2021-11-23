from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Movie, Genre, Review, Year
from .serializers import MovieSearchSerializer, MovieListSerializer, MovieSerializer, ReviewListSerializer, BestVoteMovieByYearListSerializer, RecommendMovieSerializer, GenreListSerializer, ReviewSerializer, RecentMovieByGenreListSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from collections import Counter
from itertools import islice
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model

# 연도테이블생성
@api_view(['GET'])
@permission_classes([AllowAny])
def create_year_table(request):
    batch_size = 10
    objs = (Year(id=year) for year in range(1950, 2022))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Year.objects.bulk_create(batch, batch_size)

# 검색기능 - 영화 제목으로 검색 
@api_view(['POST'])
@permission_classes([AllowAny])
def search(request):
    keyword = request.data['keyword']
    result = Movie.objects.filter(title__contains=keyword)
    serializer = MovieSearchSerializer(result, many=True)
    return Response(serializer.data)

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
def recent_movie_by_genre(request):
    genres = Genre.objects.all()
    serializer = RecentMovieByGenreListSerializer(genres, many=True)
    return Response(serializer.data)

# 평균 별점 높은 순 > 연도별 (연도별 평균 별점 순위)
@api_view(['GET'])
@permission_classes([AllowAny]) 
def best_vote_movie_by_year(request):
    # years = get_list_or_404(Year) # order_by 사용불가
    years = Year.objects.all().order_by('-id')
    serializer = BestVoteMovieByYearListSerializer(years, many=True)
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
    # token 받기 전 
    # user_pk = request.data['user'] # 5
    # User = get_user_model()
    # user = get_object_or_404(User, pk=user_pk) # test1
    # token 받은 후
    user = request.user
    print
    user = getattr(user, 'id')
    user_reviews = Review.objects.all().filter(user=user)
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
        recommend_movies_no_overlap = Movie.objects.filter(id__in=recommend_movies_no_overlap_ids) # Movie QuerySet
        
        # 4. 만약 추천 갯수가 5개 미만이면, 인기도 순(popularity), 최신 순으로 5개를 더 출력한다.
        if len(recommend_movies_no_overlap_ids) < 5:
            more = Movie.objects.order_by('-popularity', '-release_date')[:5]
            recommend_movies_no_overlap = recommend_movies_no_overlap | more
            # recommend_movies_no_overlap_ids.append(more['id']) error

        # print(recommend_movies_no_overlap_ids)
        # print(recommend_movies_no_overlap)
        
        serializers = RecommendMovieSerializer(recommend_movies_no_overlap, many=True)
        return Response(serializers.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_recommend_genre(request):
    # 장르 제외한 추천과 동일한 부분
    # token 받기 전 
    user_pk = request.data['user'] # 5
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk) # test1
    # token 받은 후
    # user = request.user
    user_reviews = Review.objects.all().filter(user=user)

    review_gte4 = user_reviews.filter(rank__gte=4)
    review_gte4_count = user_reviews.filter(rank__gte=4).count()

    if review_gte4_count >= 5:
        movie_list_gte4 = []
        for review in review_gte4:
            movie_id = getattr(review, 'movie_id') 
            if movie_id not in movie_list_gte4:
                movie_list_gte4.append(movie_id)   
        
        reviews = Review.objects.all().exclude(user=user)
        same_taste_users = []
        for movie in movie_list_gte4:
            for review in reviews:
                user_id = getattr(review, 'user_id')
                movie_id = getattr(review, 'movie_id')
                if movie_id == movie and user_id not in same_taste_users:
                    same_taste_users.append(user_id)

        recommend_movies = []
        User = get_user_model()
        for same_taste_user in same_taste_users:
            s = User.objects.get(id=same_taste_user) 
            reviews = s.user_reviews.all()
            rm = reviews.filter(user=same_taste_user).values('movie') 
            for r in rm:
                if r['movie'] not in movie_list_gte4:  
                    recommend_movies.append(r['movie'])
            recommend_movies_no_overlap_ids = list(set(recommend_movies)) 
            recommend_movies_no_overlap = Movie.objects.filter(id__in=recommend_movies_no_overlap_ids)

        if len(recommend_movies_no_overlap_ids) < 5:
            more = Movie.objects.order_by('-popularity', '-release_date')[:5]
            recommend_movies_no_overlap = recommend_movies_no_overlap | more

    #장르추가########################################################특정 사용자가 4점이상 준 리뷰들의 장르별 비율을 구한다.

    # 1. 4점 이상인 리뷰를 골라서 해당 영화 정보를 찾는다.
    genres_movie_list_gte4 = [] # [13, 24, 122, 335, 598, 1124, 4348, 489, 14]
    # 2. 해당 영화들의 장르를 담는다. (중복포함)
    for movie_id in movie_list_gte4:
        movie = Movie.objects.filter(id=movie_id) 
        genre_ids = movie.values('genre_ids') # [{'genre_ids': 18}, {'genre_ids': 35}, {'genre_ids': 10749}]>
        
        for genre_id in genre_ids:
                genres_movie_list_gte4.append(genre_id['genre_ids'])

    # 3. 장르별 갯수를 구한다.
    genre_ratio_movie_list_gte4 = dict(Counter(genres_movie_list_gte4)) # {18: 7, 35: 1, 10749: 2, 28: 2, 80: 2, 12: 1, 14: 1, 37: 1, 53: 1, 9648: 1}

    # 4. 특정 사용자가 4점 이상 준 영화와 같은 영화의 리뷰를 남긴 다른 유저를 찾는다. 
    # 5. 다른 유저의 리스트에서 높은 평점 중 내가 쓴 리뷰와 겹치지 않는 영화를 추천한다.

    # 6. 추천영화 리스트에서 해당 장르 갯수대로 하나씩 뽑는다.
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


# 북마크
@api_view(['POST'])
@permission_classes([AllowAny])
def bookmarks(request, movie_pk):
    # token 받기 전 
    # user_pk = request.data['user'] # 5
    # User = get_user_model()
    # user = get_object_or_404(User, pk=user_pk) # test1
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if user not in movie.bookmarked_users.all():
        movie.bookmarked_users.add(movie)
    else:
        movie.bookmarked_users.remove(movie)
        
    # 이 영화정보가 유저의 북마크리스트 안에 없으면 추가, 있으면 삭제
    # 이 코드가 작동하지 않는 이유가 뭔지???
    # if movie not in user.bookmarked_movies.all():
    #     user.bookmarked_movies.add(user)
    # else:
    #     user.bookmarked_movies.remove(movie)


# 리뷰리스트 및 리뷰작성(특정 영화의)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review_list_or_create(request, movie_pk):

    if request.method == 'GET':
        reviews = Review.objects.all()
        movie_reviews = reviews.filter(movie=movie_pk).order_by("created_at")
        serializer = ReviewListSerializer(movie_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method =='POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        # token 받기 전 
        # user_pk = request.data['user'] # 5
        # User = get_user_model()
        # user = get_object_or_404(User, pk=user_pk) # test1

        user = request.user
        # print(user)

        serializer = ReviewListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def review_detail_or_update_or_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # token 받기 전 
        user_pk = request.data['user'] # 5
        User = get_user_model()
        user = get_object_or_404(User, pk=user_pk) # test1
        # user = request.user
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