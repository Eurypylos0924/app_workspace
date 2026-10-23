"""관리자 화면에서 상품 및 분류를 관리하도록 등록한다."""
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 관리자 목록에 분류 ID와 이름을 표시한다.
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # 관리자 목록의 표시 열을 지정한다.
    list_display = ("id", "name", "category", "price", "stock")
    # 분류별로 필터링할 수 있도록 설정한다.
    list_filter = ("category",)
    search_fields = ("name", "description")
