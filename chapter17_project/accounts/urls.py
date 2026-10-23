"""회원가입 화면 URL을 연결한다."""
from django.urls import path
from . import views
urlpatterns = [path("signup/", views.signup, name="signup")]
