from django.urls import path
from .views import RegisterView, LoginView, RefreshView, LogoutView, UserInfoView

urlpatterns = [
    path("register/", RegisterView.as_view()),   
    path("login/", LoginView.as_view()),         
    path("refresh/", RefreshView.as_view()),     
    path("logout/", LogoutView.as_view()),       
    path("userinfo/", UserInfoView.as_view()),   
]
