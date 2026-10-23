"""제17장: 실제 HTTP 요청과 MySQL 테스트 DB를 사용하는 통합 시나리오이다.

실행: uv run pytest tests/test_integration_flow.py -v
주의: pytest-django는 별도의 테스트 데이터베이스를 만들고 삭제한다.
"""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from orders.models import Order, OrderItem, PaymentRecord
from shop.models import Category, Product


@pytest.fixture
def shopping_case(transactional_db, client):
    """테스트마다 격리된 사용자·분류·상품·로그인 상태를 생성한다."""
    # 테스트용 사용자를 생성한다. 운영 DB 사용자와 무관하다.
    user = get_user_model().objects.create_user(
        username="integration_customer", password="safe-test-password-123"
    )
    # 분류를 먼저 저장해야 상품의 외래 키가 유효해진다.
    category = Category.objects.create(name="통합 테스트 분류")
    # 가격·재고를 명시하여 검증 결과가 환경에 의존하지 않도록 한다.
    product = Product.objects.create(
        category=category, name="통합 테스트 상품", price=Decimal("15000.00"),
        stock=10, description="제17장 검증용 상품"
    )
    # 로그인 후 장바구니 및 주문 요청을 전송한다.
    client.force_login(user)
    return client, user, product


@pytest.mark.django_db(transaction=True)
def test_full_order_payment_cancel_refund_flow(shopping_case):
    """검색→장바구니→주문→결제→취소→환불→재고 복원을 확인한다."""
    client, user, product = shopping_case
    # 실제 View가 상품을 검색 결과로 반환하는지 확인한다.
    response = client.get(reverse("product_list"), {"q": "통합 테스트"})
    assert response.status_code == 200
    assert "통합 테스트 상품" in response.content.decode("utf-8")
    # 장바구니에 2개를 넣는다. URL과 폼 필드명은 기존 앱 규약을 사용한다.
    response = client.post(reverse("cart_add", args=[product.pk]), {"quantity": "2"})
    assert response.status_code == 302
    assert client.session.get("cart", {}).get(str(product.pk)) == 2
    # POST 요청으로 주문을 생성하고 MySQL 재고를 차감한다.
    response = client.post(reverse("checkout"))
    assert response.status_code == 302
    order = Order.objects.get(user=user)
    assert order.total_amount == Decimal("30000.00")
    assert OrderItem.objects.filter(order=order, product=product, quantity=2).exists()
    product.refresh_from_db()
    assert product.stock == 8
    # 교육용 모의 결제 기록이 한 건만 생성되는지 확인한다.
    response = client.post(reverse("order_pay", args=[order.pk]))
    assert response.status_code == 302
    record = PaymentRecord.objects.get(order=order)
    assert record.status == PaymentRecord.Status.PAID
    # 접수 상태의 주문을 취소하면 재고가 원래 수량으로 돌아간다.
    response = client.post(reverse("order_cancel", args=[order.pk]))
    assert response.status_code == 302
    order.refresh_from_db()
    product.refresh_from_db()
    assert order.status == Order.Status.CANCELLED
    assert product.stock == 10
    # 모의 환불은 결제 기록의 상태만 변경한다.
    response = client.post(reverse("order_refund", args=[order.pk]))
    assert response.status_code == 302
    record.refresh_from_db()
    assert record.status == PaymentRecord.Status.REFUNDED
    # 중복 취소 시도 후에도 재고가 증가하지 않아야 한다.
    client.post(reverse("order_cancel", args=[order.pk]))
    product.refresh_from_db()
    assert product.stock == 10


@pytest.mark.django_db(transaction=True)
def test_another_user_cannot_read_order(shopping_case):
    """주문 소유권 검사를 통과하지 못한 사용자는 상세 조회가 불가능하다."""
    client, owner, _ = shopping_case
    order = Order.objects.create(user=owner, total_amount=Decimal("1000.00"))
    # 다른 계정으로 전환하여 소유자만 조회 가능한지 검사한다.
    stranger = get_user_model().objects.create_user(username="other_customer")
    client.force_login(stranger)
    response = client.get(reverse("order_detail", args=[order.pk]))
    assert response.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_nonstaff_cannot_open_reports(shopping_case):
    """일반 계정이 관리자 보고서를 열 수 없음을 확인한다."""
    client, _, _ = shopping_case
    response = client.get(reverse("reports:dashboard"))
    assert response.status_code == 302
    assert "/accounts/login/" in response.url
