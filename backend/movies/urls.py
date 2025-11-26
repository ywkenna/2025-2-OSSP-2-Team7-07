from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:id>/', views.detail, name='detail'),
    path('score/', views.score, name='score'),
    path('recommend/', views.recommend, name='recommend'),
    path('search/', views.search, name='search'),
]