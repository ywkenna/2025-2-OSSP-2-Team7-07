from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies_api, name='movies_api'),
    path('search/', views.movies_search_api, name='search'),
    path('<int:id>/', views.movie_detail_api),

    # ✅ 이 라인이 꼭 있어야 함
    path('<int:movie_id>/comments/', views.comment_create_api, name='comment_create'),

    path('list/', views.movies_api),
    path('recommend/api/', views.movies_recommend_api, name='movies_recommend'),

]

