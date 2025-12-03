from django.urls import path
from . import views

urlpatterns = [
    # HTML 페이지
    path('', views.home, name='home'),
    path('movie/<int:id>/', views.detail, name='detail'),
    path('score/', views.score, name='score'),
    path('recommend/', views.recommend, name='recommend'),
    path('search/', views.movies_search_api, name='movies_search_api'),

    # JSON API (여기!!!) 

    path('list/', views.movies_api, name='movies_api'),
    path("<int:id>/", views.movie_detail_api),
]

