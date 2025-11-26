from django.urls import path
from .views import RegisterView, LoginView, RefreshView, LogoutView, UserInfoView, UpdateLikeView, LikeView

urlpatterns = [
    path("register/", RegisterView.as_view()),   
    path("login/", LoginView.as_view()),         
    path("refresh/", RefreshView.as_view()),     
    path("logout/", LogoutView.as_view()),       
    path("userinfo/", UserInfoView.as_view()),
    path("like/<int:movie_id>/", UpdateLikeView.as_view()),
    path("like/", LikeView.as_view()),
]
