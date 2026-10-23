import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from shop.models import Category, Product
from orders.models import Order, OrderItem

@pytest.fixture
def buyer(db):
    # 주문을 생성할 일반 사용자를 준비한다.
    return get_user_model().objects.create_user(username="buyer13", password="Testpass123!")

@pytest.fixture
def product(db):
    # 각 테스트는 격리된 테스트 DB에서 재고 5개의 상품을 생성한다.
    category = Category.objects.create(name="제13장 분류")
    return Product.objects.create(category=category, name="실습 상품", price=Decimal("12000.00"), stock=5)

@pytest.mark.django_db(transaction=True)
def test_checkout_creates_order_and_decreases_stock(client, buyer, product):
    # 로그인 사용자에게 장바구니 수량 2개를 지정한다.
    client.force_login(buyer)
    session = client.session
    session["cart"] = {str(product.pk): 2}
    session.save()
    response = client.post(reverse("checkout"))
    assert response.status_code == 302
    order = Order.objects.get(user=buyer)
    assert order.total_amount == Decimal("24000.00")
    assert OrderItem.objects.get(order=order).quantity == 2
    product.refresh_from_db()
    assert product.stock == 3
    assert client.session.get("cart") == {}

@pytest.mark.django_db(transaction=True)
def test_checkout_rejects_insufficient_stock(client, buyer, product):
    # 재고보다 많은 수량은 주문·재고 차감 없이 거절한다.
    client.force_login(buyer)
    session = client.session
    session["cart"] = {str(product.pk): 6}
    session.save()
    response = client.post(reverse("checkout"))
    assert response.status_code == 302
    assert not Order.objects.exists()
    product.refresh_from_db()
    assert product.stock == 5

@pytest.mark.django_db
def test_order_detail_is_private(client, buyer, product):
    # 다른 사용자가 주문 상세 URL을 직접 요청해도 404를 반환한다.
    owner = get_user_model().objects.create_user(username="owner13", password="Testpass123!")
    order = Order.objects.create(user=owner, total_amount=Decimal("0.00"))
    client.force_login(buyer)
    response = client.get(reverse("order_detail", args=[order.pk]))
    assert response.status_code == 404

@pytest.mark.django_db
def test_checkout_requires_login(client):
    # 비로그인 사용자는 주문 확인 화면에 접근할 수 없다.
    response = client.get(reverse("checkout"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.url
