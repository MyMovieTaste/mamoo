from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 회원가입
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)
    # review_count = serializers.IntegerField(source='review_set.count', read_only=True) # 영화에 달린 모든 리뷰수

# 프로필 정보
class ProfileSerializer(serializers.ModelSerializer):
    # profile_user = obj.profile_user
    # followings = serializers.profile_user.followings.all() # 유저 팔로잉 수
    # followers = profile_user.followers.all() # 유저 팔로워 수
    # reviews = profile_user.review_set.all() # 유저가 작성한 리뷰
    # bookmarks = profile_user.bookmakred_movies.all() # 유저가 북마크한 영화
    # followings = profile_user.followings.all() # 유저 팔로잉 수
    # followers = profile_user.followers.all() # 유저 팔로워 수
    # reviews = profile_user.review_set.all() # 유저가 작성한 리뷰
    # bookmarks = profile_user.bookmakred_movies.all() # 유저가 북마크한 영화
    
    class Meta:
        model = User
        fields = '__all__'
