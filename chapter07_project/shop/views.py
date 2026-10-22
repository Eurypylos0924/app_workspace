# MySQL에서 상품을 읽어 화면에 보여주는 뷰입니다.
from django.shortcuts import render

from .models import Product


def product_list(request):
    # ORM으로 상품 전체를 조회합니다. (SQL의 SELECT * 와 같은 역할)
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})
