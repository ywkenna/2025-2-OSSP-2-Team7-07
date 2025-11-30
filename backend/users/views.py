from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import RegisterSerializer, UserPublicSerializer
from users.models import TAGS
from movies.models import MovieData

# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# 로그인
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserPublicSerializer(self.user).data
        return data

class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

# 토큰 갱신
class RefreshView(TokenRefreshView):
    pass

# 로그아웃
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"detail": "Logged out"})


# 사용자 정보
class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserPublicSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user

        # User 정보 수정
        for field in ["first_name", "email"]:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()

        # Profile 정보 수정
        profile = user.profile
        if "english_level" in request.data:
            profile.english_level = request.data["english_level"]

        if "like_movies" in request.data:
            profile.like_movies.set(request.data["like_movies"])

        if "like_tags" in request.data:
            tags = request.data["like_tags"]
            for tag in tags:
                if tag not in TAGS:
                    return Response({"detail": f"Invalid tag: {tag}"}, status=400)
            profile.like_tags = tags
            
        profile.save()

        return Response(UserPublicSerializer(user).data)

class UpdateLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id):
        try:
            movie = MovieData.objects.get(id=movie_id)
        except MovieData.DoesNotExist:
            return Response({"detail": "Movie not found"}, status=404)

        profile = request.user.profile
        profile.like_movies.add(movie)
        return Response({"detail": "Liked"})

    def delete(self, request, movie_id):
        try:
            movie = MovieData.objects.get(id=movie_id)
        except MovieData.DoesNotExist:
            return Response({"detail": "Movie not found"}, status=404)

        profile = request.user.profile
        profile.like_movies.remove(movie)
        return Response({"detail": "Unliked"})
    
class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        movies = profile.like_movies.all()

        movie_list = [
            {
                "id": movie.id,
                "title_ko": movie.title_ko,
            }
            for movie in movies
        ]

        return Response(movie_list)