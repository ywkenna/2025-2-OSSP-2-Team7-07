from django.urls import path
from . import views

urlpatterns = [
    # HTML 페이지
    path('', views.home, name='home'),
    path('movie/<int:id>/', views.detail, name='detail'),
    path('score/', views.score, name='score'),

    # 추천 API는 반드시 detail 패턴보다 위
    path('recommend/api/', views.movies_recommend_api),

    # 검색 API
    path('search/', views.movies_search_api, name='search'),

    # 리스트 API
    path('list/', views.movies_api, name='movies_api'),

    # 단일 영화 상세 API — ★맨 마지막★
    path('<int:id>/', views.movie_detail_api),
]

