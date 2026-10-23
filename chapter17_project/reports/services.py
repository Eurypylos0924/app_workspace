"""제16장 주문 통계 집계 로직이다. DB 접근과 화면 출력을 분리한다."""
from decimal import Decimal
from django.db.models import Count, Sum
from orders.models import Order, PaymentRecord


def get_order_summary():
    """전체 주문 수, 취소 수, 모의 결제 합계를 집계한다."""
    # 주문 상태와 무관하게 전체 주문 건수를 집계한다.
    total_orders = Order.objects.count()
    # 취소 상태인 주문만 별도로 집계한다.
    cancelled_orders = Order.objects.filter(status=Order.Status.CANCELLED).count()
    # 실제 매출이 아닌 '모의 결제 완료' 상태의 기록만 합산한다.
    paid_amount = PaymentRecord.objects.filter(
        status=PaymentRecord.Status.PAID
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    # 템플릿과 테스트가 동일한 키를 사용하도록 딕셔너리로 반환한다.
    return {
        "total_orders": total_orders,
        "cancelled_orders": cancelled_orders,
        "paid_amount": paid_amount,
    }


def get_status_breakdown():
    """상태별 주문 수를 목록으로 반환한다."""
    # values()와 annotate()를 조합하여 DB에서 GROUP BY를 수행한다.
    return list(
        Order.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
