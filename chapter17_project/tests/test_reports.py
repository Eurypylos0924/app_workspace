"""제16장 운영 통계 및 CSV 접근 권한을 검사한다."""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from orders.models import Order, PaymentRecord
from reports.services import get_order_summary


@pytest.fixture
def staff_user(db):
    # 보고서에 접근 가능한 관리자 계정을 생성한다.
    return get_user_model().objects.create_user(
        username="report_admin", password="test-password-123", is_staff=True
    )


@pytest.fixture
def normal_user(db):
    # 접근 제한을 검증하기 위한 일반 계정을 생성한다.
    return get_user_model().objects.create_user(
        username="report_user", password="test-password-123"
    )


@pytest.mark.django_db
def test_summary_aggregates_paid_amount(staff_user):
    # 모의 결제 완료된 주문을 생성한다.
    order = Order.objects.create(user=staff_user, total_amount=Decimal("12000.00"))
    PaymentRecord.objects.create(order=order, amount=Decimal("12000.00"))
    # 결제 기록이 있는 주문의 금액만 합산되는지 확인한다.
    result = get_order_summary()
    assert result["total_orders"] == 1
    assert result["cancelled_orders"] == 0
    assert result["paid_amount"] == Decimal("12000.00")


@pytest.mark.django_db
def test_staff_can_open_dashboard(client, staff_user):
    # 관리자 계정으로 로그인하면 대시보드가 열려야 한다.
    client.force_login(staff_user)
    response = client.get(reverse("reports:dashboard"))
    assert response.status_code == 200
    assert "주문 운영 현황" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_normal_user_cannot_open_dashboard(client, normal_user):
    # 일반 계정은 보고서 화면에 접근할 수 없다.
    client.force_login(normal_user)
    response = client.get(reverse("reports:dashboard"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_staff_can_download_csv(client, staff_user):
    # 관리자에게만 CSV 다운로드가 허용되어야 한다.
    client.force_login(staff_user)
    response = client.get(reverse("reports:orders_csv"))
    assert response.status_code == 200
    assert response.content.startswith(b"\xef\xbb\xbf")
    assert "text/csv" in response["Content-Type"]


@pytest.mark.django_db
def test_normal_user_cannot_download_csv(client, normal_user):
    # 일반 계정의 CSV 다운로드 요청은 로그인 경로로 리다이렉트한다.
    client.force_login(normal_user)
    response = client.get(reverse("reports:orders_csv"))
    assert response.status_code == 302
