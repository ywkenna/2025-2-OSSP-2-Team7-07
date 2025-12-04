from django.urls import path
from . import views

urlpatterns = [
    
    #코멘트 작성 API
    path('<int:movie_id>/comment/', views.comment_create_api),

    # 추천 API
    path('recommend/api/', views.movies_recommend_api),

    # 검색 API
    path('search/', views.movies_search_api, name='search'),

    # 리스트 API
    path('list/', views.movies_api, name='movies_api'),

    # 단일 영화 상세 API
    path('<int:id>/', views.movie_detail_api),
]

