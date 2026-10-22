# Django 화면이 MySQL 데이터를 잘 보여주는지 확인하는 뷰 테스트입니다.
import pytest
from django.urls import reverse

from shop.models import Product


@pytest.mark.django_db
def test_product_list_page(client):
    # 상품이 있을 때 목록 화면에 이름이 나오는지 확인합니다.
    Product.objects.create(name="노트북", price=1200000, stock=5)
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert "노트북" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_empty_product_list(client):
    # 상품이 없을 때 안내 문구가 나오는지 확인합니다.
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert "상품이 없습니다." in response.content.decode("utf-8")
