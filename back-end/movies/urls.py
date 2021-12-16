from django.urls import path
from . import views

urlpatterns = [
    # 영화 제목으로 검색하기
    path('search/', views.search), 

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

    # 영화 추천
    path('movie_recommend/', views.movie_recommend), 

    # 내가 4점이상 리뷰 준 영화의 장르비율 => 미사용
    # path('movie_mypick_genre_ratio/', views.movie_mypick_genre_ratio), 
    
    # 리뷰: 보기 쓰기 업데이트 삭제
    path('<int:movie_pk>/reviews/', views.review_list_or_create), # get, post
    path('reviews/<int:review_pk>/', views.review_detail_or_update_or_delete), # get, put, delete

    # 연도테이블 생성 => 미사용
    # path('create_year_table/', views.create_year_table), 
  ]
