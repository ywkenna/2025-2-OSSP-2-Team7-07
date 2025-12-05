from django.urls import path
from . import views

from .views import RegisterView, LoginView, RefreshView, LogoutView, UserInfoView, UpdateLikeView

urlpatterns = [
    path("register/", RegisterView.as_view()),      # POST 회원가입
    path("login/", LoginView.as_view()),            # POST 로그인
    path("logout/", LogoutView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("save_score/", views.save_score),      
    path("userinfo/", UserInfoView.as_view()),      # GET 사용자 정보, PATCH 수정
    path("like/<int:movie_id>/", UpdateLikeView.as_view()), # POST 영화 찜, DELETE 취소
]
