from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

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


# 사용자 정보 반환/수정
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

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]
            
        profile.save()

        return Response(UserPublicSerializer(user).data)

# 영화 찜/취소
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_score(request):
    user = request.user
    exam_type = request.data.get("type")
    score = float(request.data.get("score", 0))

    # CEFR 매핑
    def convert_to_cefr(type, score):
        if type == "toeic":
            if score >= 945: return 5
            if score >= 785: return 4
            if score >= 550: return 3
            if score >= 225: return 2
            return 1

        if type == "toefl":
            if score >= 95: return 5
            if score >= 72: return 4
            if score >= 42: return 3
            return 2

        if type == "ielts":
            if score > 8.0: return 5
            if score >= 7.0: return 4
            if score >= 5.5: return 3
            if score >= 4.0: return 2
            if score >= 2.5: return 1
            return 0

        return 0

    level = convert_to_cefr(exam_type, score)
    user.english_level = level
    user.save()

    return Response({
        "message": "Saved",
        "level": level
    })
