from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def profile(request, username):
    """프로필 페이지 기능"""
    User = get_user_model()
    profile_user = User.objects.get(username=username) 
    serializer = ProfileSerializer(profile_user) # object로 넣어야
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def follow(request, user_pk):
    """팔로우 기능"""
    User = get_user_model()
    you = get_object_or_404(User, pk=user_pk)
    me = request.user
    if you not in me.followings.all():
        me.followings.add(you)
    else:
        me.followings.remove(you)
    data = {
        'message' : 'follow!'
    }
    return JsonResponse(data=data)
    

@api_view(['POST'])
@permission_classes([AllowAny])  # 회원가입의 경우 로그인 전이기 때문에 permisson 허가
def signup(request):
    """회원가입 기능"""
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
	# 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
    
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)