# 관리자 화면에서 카테고리와 상품을 관리할 수 있게 등록합니다.
from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock")
    # 오른쪽에 카테고리별 필터를 보여줍니다.
    list_filter = ("category",)
    search_fields = ("name",)
