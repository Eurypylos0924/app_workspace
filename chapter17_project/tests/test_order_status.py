"""주문 취소, 중복 취소 방지, 권한 및 상태 전이를 검증한다."""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from orders.models import Order, OrderItem
from orders.services import cancel_order, confirm_order
from shop.models import Category, Product

@pytest.fixture
def sample(db):
    # 격리된 테스트 DB에 사용자·상품·주문을 준비한다.
    user = get_user_model().objects.create_user(username="buyer14", password="Testpass123!")
    category = Category.objects.create(name="제14장 카테고리")
    product = Product.objects.create(category=category, name="취소 검증 상품", price=Decimal("10000"), stock=3)
    order = Order.objects.create(user=user, total_amount=Decimal("20000"))
    OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=2, subtotal=Decimal("20000"))
    return user, product, order

@pytest.mark.django_db(transaction=True)
def test_cancel_restores_stock_once(sample):
    user, product, order = sample
    # 정상 취소 후 주문 상태와 재고가 동시에 바뀌는지 확인한다.
    cancel_order(order.pk, user)
    order.refresh_from_db(); product.refresh_from_db()
    assert order.status == Order.Status.CANCELLED
    assert order.cancelled_at is not None
    assert product.stock == 5
    # 두 번째 취소는 실패하며 재고가 다시 증가하지 않아야 한다.
    with pytest.raises(ValidationError):
        cancel_order(order.pk, user)
    product.refresh_from_db()
    assert product.stock == 5

@pytest.mark.django_db(transaction=True)
def test_other_user_cannot_cancel(sample):
    _, product, order = sample
    other = get_user_model().objects.create_user(username="other14", password="Testpass123!")
    with pytest.raises(ValidationError):
        cancel_order(order.pk, other)
    product.refresh_from_db()
    assert product.stock == 3

@pytest.mark.django_db(transaction=True)
def test_confirm_requires_staff_and_blocks_cancel(sample):
    user, product, order = sample
    with pytest.raises(ValidationError):
        confirm_order(order.pk, user)
    admin = get_user_model().objects.create_user(username="staff14", password="Testpass123!", is_staff=True)
    confirm_order(order.pk, admin)
    with pytest.raises(ValidationError):
        cancel_order(order.pk, user)
    product.refresh_from_db()
    assert product.stock == 3

@pytest.mark.django_db
def test_cancel_requires_post_and_login(client, sample):
    user, _, order = sample
    # 인증되지 않은 사용자는 로그인 페이지로 이동한다.
    response = client.post(reverse("order_cancel", args=[order.pk]))
    assert response.status_code == 302
    client.force_login(user)
    # GET으로는 상태를 변경할 수 없다.
    response = client.get(reverse("order_cancel", args=[order.pk]))
    assert response.status_code == 405
