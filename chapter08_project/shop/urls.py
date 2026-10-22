# shop 앱의 URL 설정입니다.
from django.urls import path

from . import views

# app_name: 템플릿에서 {% url 'shop:product_list' %} 처럼 이름 앞에 붙이는 이름표입니다.
app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
]
