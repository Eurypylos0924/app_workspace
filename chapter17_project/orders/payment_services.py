"""외부 PG 없이 동작하는 교육용 모의 결제 서비스이다."""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from .models import Order, PaymentRecord

@transaction.atomic
def simulate_payment(order_id, user):
    """본인의 접수 주문을 한 번만 모의 결제한다."""
    # 주문 행 잠금으로 동일 주문의 동시 결제 요청을 직렬화한다.
    order = Order.objects.select_for_update().filter(pk=order_id, user=user).first()
    if order is None:
        raise ValidationError("본인의 주문을 찾을 수 없습니다.")
    # 취소 또는 확인 상태 주문은 이 실습에서 결제할 수 없다.
    if order.status != Order.Status.PENDING:
        raise ValidationError("접수 상태의 주문만 모의 결제할 수 있습니다.")
    # 기존 기록이 있으면 새 기록을 생성하지 않아 중복 결제를 방지한다.
    if PaymentRecord.objects.filter(order=order).exists():
        raise ValidationError("이미 모의 결제가 처리된 주문입니다.")
    # 금액은 브라우저 입력이 아니라 주문 DB에 저장된 값을 사용한다.
    return PaymentRecord.objects.create(order=order, amount=order.total_amount)

@transaction.atomic
def simulate_refund(order_id, user):
    """취소된 주문의 모의 결제 기록을 환불 완료로 변경한다."""
    # 실제 금전 이동은 없으며 재고 복원은 기존 cancel_order가 담당한다.
    order = Order.objects.select_for_update().filter(pk=order_id, user=user).first()
    if order is None or order.status != Order.Status.CANCELLED:
        raise ValidationError("취소된 본인 주문만 모의 환불할 수 있습니다.")
    record = PaymentRecord.objects.select_for_update().filter(order=order).first()
    if record is None or record.status != PaymentRecord.Status.PAID:
        raise ValidationError("환불할 모의 결제 기록이 없습니다.")
    record.status = PaymentRecord.Status.REFUNDED
    record.refunded_at = timezone.now()
    record.save(update_fields=["status", "refunded_at"])
    return record
