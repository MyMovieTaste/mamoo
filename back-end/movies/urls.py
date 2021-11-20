from django.urls import path
from . import views

urlpatterns = [
    # 특정 영화 셋 보여주기 
    path('', views.movie_list), 
    # 장르별 최신 개봉영화
    path('recent_movie_by_genre_list/', views.recent_movie_by_genre_list), 
    # 특정 영화의 상세 정보를 보여주기 
    path('<int:movie_pk>/', views.get_details), 
    # 장르 리스트
    path('genre_list/', views.genre_list), 
    # 영화 추천
    path('movie_recommend/', views.movie_recommend), 
    # 리뷰: 보기 쓰기 업데이트 삭제
    path('<int:movie_pk>/reviews/', views.review_list_or_create), # get, post
    # path('<int:movie_pk>/reviews/<int:review_pk>/', views.review_detail_or_update_or_delete), # get, put, delete

    # # (리뷰의)댓글: 보기 쓰기 삭제
    # path('/<int:movie_pk>/reviews/<int:review_pk>/comments/', views.comment_list_or_create), # get, post
    # path('/<int:movie_pk>/reviews/<int:review_pk>/comments/<int:comment_pk>/', views.comment_detail_or_update_or_delete) # get, post, put, delete
  ]
