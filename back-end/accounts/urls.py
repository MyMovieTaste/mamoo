from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 회원가입
    path('signup/', views.signup),
    # jwt 발급
    path('api-token-auth/', obtain_jwt_token),
    # 프로필
    path('<username>/', views.profile),
    # 팔로우
    path('<int:user_pk>/follow/', views.follow),
]