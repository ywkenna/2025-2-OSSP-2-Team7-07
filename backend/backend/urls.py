
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies.views import frontend_home
from django.views.generic import TemplateView

urlpatterns = [
    path('', frontend_home),   # 기존 홈
    path('admin/', admin.site.urls),

    # API
    path("api/movies/", include("movies.urls")),
    path("api/users/", include("users.urls")),

    # ★ 정적 페이지 라우팅 추가
    path("signup/", TemplateView.as_view(template_name="signup.html")),
    path("login/", TemplateView.as_view(template_name="login.html")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
