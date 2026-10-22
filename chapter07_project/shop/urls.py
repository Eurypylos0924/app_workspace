# shop 앱의 URL을 뷰와 연결합니다.
from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
]
