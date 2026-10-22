"""프로젝트 전체 URL 설정."""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include


# 1장 확인용 홈 화면
def home(request):
    return HttpResponse("<h1>Chapter 01 Django 개발환경</h1><p>Python 3.12 + uv</p>")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("boards/", include("boards.urls")),
    path("accounts/", include("accounts.urls")),
    path("products/", include("products.urls")),
    path("", home, name="home"),
]
