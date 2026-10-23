"""Django 테스트 클라이언트로 상품 목록/상세 페이지를 검증한다."""
from decimal import Decimal
import pytest
from django.urls import reverse
from shop.models import Category, Product

@pytest.mark.django_db
def test_product_list(client):
    category = Category.objects.create(name="도서")
    Product.objects.create(category=category, name="Django 입문", price=Decimal("25000.00"))
    # HTTP 요청을 실제 웹 브라우저 없이 시뮬레이션한다.
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert "Django 입문" in response.content.decode("utf-8")

@pytest.mark.django_db
def test_product_detail_404(client):
    # 존재하지 않는 상품은 404 응답을 반환해야 한다.
    response = client.get(reverse("product_detail", args=[999999]))
    assert response.status_code == 404
