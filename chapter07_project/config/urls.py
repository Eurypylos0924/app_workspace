# 전체 URL 설정입니다. shop 앱의 URL을 여기에 연결합니다.
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 빈 경로("")로 들어오면 shop 앱의 URL 설정으로 넘깁니다.
    path("", include("shop.urls")),
]
