# 상품 목록과 상세 화면을 보여주는 뷰입니다.
from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    # select_related: 카테고리를 JOIN 으로 한 번에 가져와 쿼리 횟수를 줄입니다.
    products = Product.objects.select_related("category").all()
    return render(request, "shop/product_list.html", {"products": products})


def product_detail(request, pk):
    # 상품이 없으면 서버 오류 대신 HTTP 404 를 돌려줍니다.
    product = get_object_or_404(
        Product.objects.select_related("category"), pk=pk
    )
    return render(request, "shop/product_detail.html", {"product": product})
