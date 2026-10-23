"""pytest-django로 URL, 템플릿, 인증, 세션 장바구니를 검증한다."""
from decimal import Decimal
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from shop.models import Category, Product

@pytest.fixture
def product(db):
    # DB 테스트마다 독립된 테스트 데이터베이스에 분류와 상품을 만든다.
    category = Category.objects.create(name="전자제품")
    return Product.objects.create(category=category, name="노트북", price=Decimal("1200000.00"), stock=3)

def test_product_list(client, product):
    # 목록 URL이 200을 반환하고 상품명이 화면에 표시되는지 확인한다.
    response = client.get(reverse("product_list"))
    assert response.status_code == 200
    assert "노트북" in response.content.decode()

def test_product_detail_404(client, db):
    # 존재하지 않는 상품 번호는 404를 반환해야 한다.
    assert client.get(reverse("product_detail", args=[99999])).status_code == 404

def test_cart_add_requires_post(client, product):
    # 세션 변경은 GET이 아닌 POST로만 허용한다.
    assert client.get(reverse("cart_add", args=[product.pk])).status_code == 405
    response = client.post(reverse("cart_add", args=[product.pk]))
    assert response.status_code == 302
    assert client.session["cart"][str(product.pk)] == 1

def test_signup(client, db):
    # 유효한 회원가입 입력으로 새 계정이 생성되는지 확인한다.
    response = client.post(reverse("signup"), {"username":"demo_user", "email":"demo@example.com", "password1":"TestPass123!unique", "password2":"TestPass123!unique"})
    assert response.status_code == 302
    assert User.objects.filter(username="demo_user").exists()

def test_product_create_requires_login(client, db):
    # 비로그인 사용자는 상품 등록 페이지 대신 로그인 페이지로 이동한다.
    response = client.get(reverse("product_create"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.url
