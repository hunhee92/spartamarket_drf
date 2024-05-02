from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from .serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer, UserDeleteSerializer
from .models import User

# Create your views here.


class AccountSiginAPIView(APIView):  # 회원가입
    def post(self, request):
        print("회원가입")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):  # 유저 프로필
        print("유저 프로필")
        user_profile = get_object_or_404(User, username=username)
        serializer = UserSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request, username):  # 로그아웃
        print("로그아웃")
        refresh_token = request.data.get("refresh_token")
        if refresh_token is None:
            print("로그아웃 실패: refresh_token이 제공되지 않음")
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("로그아웃 성공")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, username):  # 회원 정보 수정
        print(username, request.user.username)
        user_profile = get_object_or_404(User, username=username)
        serializer = UserUpdateSerializer(
            user_profile, data=request.data)
        if username == request.user.username:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DelteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, username):
        print("del 들어왓니")
        user = get_object_or_404(User, username=username)
        serializer = UserDeleteSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):  # 비밀번호 검증
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # 삭제 성공
        # 검증 실패
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        print("비밀번호 변경api")
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
