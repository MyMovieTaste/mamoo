from django.contrib.auth.models import User
from django.db.models import fields
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
# StringRelatedField
class ProfileSerializer(serializers.ModelSerializer):
    # bookmarked_movies = serializers.StringRelatedField(many=True)
    followings = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True) # 유저 팔로워 수
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'followings_count','followings','followers_count', 'followers','bookmarked_movies',)
