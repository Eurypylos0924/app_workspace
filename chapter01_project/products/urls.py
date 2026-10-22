# URL 경로를 등록하는 함수를 가져온다
from django.urls import path

# 현재 앱ㅇ의 화면 함수를 가져온다.
from . import views

# URL 이름의 충돌을 방지하기 위해 앱 이름을 지정한다.
app_name = "products"

# 앱의 기본 화면 URL을 등록한다
urlpatterns = [
    path("", views.home, name="home"),
]