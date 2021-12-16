from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 회원가입
    path('signup/', views.signup),
    # jwt 토큰
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 프로필
    path('<username>/', views.profile),
    # 팔로우
    path('<int:user_pk>/follow/', views.follow),
]