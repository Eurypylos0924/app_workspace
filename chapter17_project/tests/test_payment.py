"""제15장 모의 결제·환불의 핵심 규칙을 검증한다."""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from orders.models import Order, PaymentRecord
from orders.payment_services import simulate_payment, simulate_refund

@pytest.fixture
def customer(db):
    # 테스트 전용 사용자를 생성한다.
    return get_user_model().objects.create_user(username="buyer15", password="test-pass-123")

@pytest.fixture
def order(customer):
    # 실제 결제 없이 주문 상태 검증에 필요한 데이터만 생성한다.
    return Order.objects.create(user=customer, total_amount=Decimal("25000.00"))

@pytest.mark.django_db(transaction=True)
def test_payment_is_recorded_once(order, customer):
    record = simulate_payment(order.pk, customer)
    assert record.amount == Decimal("25000.00")
    with pytest.raises(ValidationError):
        simulate_payment(order.pk, customer)
    assert PaymentRecord.objects.filter(order=order).count() == 1

@pytest.mark.django_db(transaction=True)
def test_other_user_cannot_pay(order):
    other = get_user_model().objects.create_user(username="other15", password="test-pass-123")
    with pytest.raises(ValidationError):
        simulate_payment(order.pk, other)

@pytest.mark.django_db(transaction=True)
def test_refund_requires_cancelled_order(order, customer):
    simulate_payment(order.pk, customer)
    with pytest.raises(ValidationError):
        simulate_refund(order.pk, customer)
    order.status = Order.Status.CANCELLED
    order.save(update_fields=["status"])
    record = simulate_refund(order.pk, customer)
    assert record.status == PaymentRecord.Status.REFUNDED
    with pytest.raises(ValidationError):
        simulate_refund(order.pk, customer)
