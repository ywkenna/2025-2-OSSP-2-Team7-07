from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, UpdateLikeView
urlpatterns = [
    path("register/", RegisterView.as_view()),      # POST 회원가입
    path("login/", LoginView.as_view()),            # POST 로그인
    path("userinfo/", UserInfoView.as_view()),      # GET 사용자 정보, PATCH 수정
    path("like/<int:movie_id>/", UpdateLikeView.as_view()), # POST 영화 찜, DELETE 취소
]