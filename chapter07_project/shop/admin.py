# Django 관리자 화면(admin)에서 상품을 관리할 수 있게 등록합니다.
from django.contrib import admin

# models.py 에서 만든 Product 모델을 가져옵니다.
from .models import Product


# @admin.register(Product): Product 모델을 관리자 화면에 등록합니다.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 목록 화면에 보여줄 열(필드)
    list_display = ("id", "name", "price", "stock")
    # 이름으로 검색할 수 있게 합니다.
    search_fields = ("name",)
