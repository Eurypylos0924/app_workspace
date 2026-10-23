"""pytest-django로 장바구니 세션과 재고·수량 검증을 테스트한다."""
from decimal import Decimal
import pytest
from django.urls import reverse
from shop.models import Category, Product

@pytest.fixture
def product(db):
    # 테스트용 MySQL DB에 분류와 재고가 있는 상품을 생성한다.
    category = Category.objects.create(name="도서")
    return Product.objects.create(category=category, name="파이썬 교재", price=Decimal("15000.00"), stock=5)

def test_add_and_total(client, product):
    # 상품 2개를 담으면 세션 수량과 합계가 일치해야 한다.
    response = client.post(reverse("cart_add", args=[product.pk]), {"quantity": "2"})
    assert response.status_code == 302
    assert client.session["cart"][str(product.pk)] == 2
    page = client.get(reverse("cart_detail"))
    assert page.context["total"] == Decimal("30000.00")

def test_update_quantity(client, product):
    # 기존 수량을 변경할 때에는 덮어써야 한다.
    client.post(reverse("cart_add", args=[product.pk]))
    client.post(reverse("cart_update", args=[product.pk]), {"quantity": "3"})
    assert client.session["cart"][str(product.pk)] == 3

def test_invalid_quantity_preserves_cart(client, product):
    # 음수, 0, 문자는 수량으로 허용하지 않는다.
    for invalid in ["0", "-1", "abc", "100"]:
        client.post(reverse("cart_add", args=[product.pk]), {"quantity": invalid})
    assert client.session.get("cart", {}) == {}

def test_stock_limit(client, product):
    # 재고보다 큰 수량은 장바구니에 저장하지 않는다.
    client.post(reverse("cart_add", args=[product.pk]), {"quantity": "6"})
    assert client.session.get("cart", {}) == {}

def test_remove_and_clear(client, product):
    # 품목 삭제와 전체 비우기가 세션에 반영되어야 한다.
    client.post(reverse("cart_add", args=[product.pk]))
    client.post(reverse("cart_remove", args=[product.pk]))
    assert client.session["cart"] == {}
    client.post(reverse("cart_add", args=[product.pk]))
    client.post(reverse("cart_clear"))
    assert "cart" not in client.session

def test_post_only(client, product):
    # GET 요청으로 장바구니를 변경하지 못하도록 막는다.
    assert client.get(reverse("cart_add", args=[product.pk])).status_code == 405
    assert client.get(reverse("cart_clear")).status_code == 405
