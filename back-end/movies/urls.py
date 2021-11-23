from django.urls import path
from . import views

urlpatterns = [
    # 영화 제목으로 검색하기
    path('search/', views.search), 
    path('create_year_table/', views.create_year_table), 

    # 전체 영화리스트 보여주기 
    path('', views.movie_list), 
    # 장르별 최신 개봉영화
    path('recent_movie_by_genre/', views.recent_movie_by_genre), 
    # 연도별 평점순 영화
    path('best_vote_movie_by_year/', views.best_vote_movie_by_year), 

    # 영화 상세 정보를 보여주기 
    path('<int:movie_pk>/', views.get_details), 
    
    # 북마크
    path('<int:movie_pk>/bookmarks/', views.bookmarks),

    # 장르 리스트
    path('genre_list/', views.genre_list), 

    # 영화 추천
    path('movie_recommend/', views.movie_recommend), 
    # 영화 추천(장르 추가)
    path('movie_recommend_genre/', views.movie_recommend_genre), 
    
    # 리뷰: 보기 쓰기 업데이트 삭제
    path('<int:movie_pk>/reviews/', views.review_list_or_create), # get, post
    path('reviews/<int:review_pk>/', views.review_detail_or_update_or_delete), # get, put, delete
    # path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail_or_update_or_delete), # get, put, delete

    # # (리뷰의)댓글: 보기 쓰기 삭제
    # path('/<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comment_list_or_create), # get, post
    # path('/<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail_or_update_or_delete) # get, post, put, delete

  ]
