from django.urls import path
from . import views

urlpatterns = [
    # 특정 영화 셋 보여주기 
    path('top_rated/', views.top_rated_movie_list), 
    # 특정 영화의 상세 정보를 보여주기 
    path('<int:pk>/', views.get_details), 
    # path('<int:movie_pk>/', views.movie_detail), 

    # 리뷰: 보기 쓰기 업데이트 삭제
    #path('reviews/', views.review_list_or_create), 
    #path('reviews/<int:review_pk>/', views.review_detail_or_update_or_delete),

    # 리뷰 댓글: 보기 쓰기 삭제
    #path('reviews/<int:review_pk>/comments/', views.comment_list_or_create),
    #path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.review_detail_or_delete)   
  ]
