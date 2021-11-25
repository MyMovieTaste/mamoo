from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

# 프로필
@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request, username):
    # token 받기 전 
    # user_pk = request.data['user'] # 5
    # User = get_user_model()
    # user = get_object_or_404(User, pk=user_pk) # test1
    User = get_user_model()
    profile_user = User.objects.get(username=username) 
    serializer = ProfileSerializer(profile_user) # object로 넣어야
    return Response(serializer.data)

# 팔로우
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def follow(request, user_pk):
    # token 받기 전 
    # my_pk = request.data['user'] # 5
    User = get_user_model()
    # me = get_object_or_404(User, pk=my_pk) 
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
    

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
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