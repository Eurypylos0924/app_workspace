from django.conf import settings
from django.db import models
from shop.models import Product

class Order(models.Model):
    # 주문 상태는 고정된 선택지로 관리하여 잘못된 문자열 저장을 방지한다.
    class Status(models.TextChoices):
        PENDING = "pending", "접수"
        CONFIRMED = "confirmed", "확인"
        CANCELLED = "cancelled", "취소"

    # 기존 제13장 주문에는 기본값 pending을 부여한다.
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    # 취소 시각은 취소된 주문에만 저장한다.
    cancelled_at = models.DateTimeField(null=True, blank=True)
    # 주문은 로그인한 사용자 한 명에게 귀속된다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    # 주문 완료 당시의 전체 결제 예정 금액을 보존한다.
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"주문 #{self.pk}"

class OrderItem(models.Model):
    # 하나의 주문은 여러 주문 상품을 포함한다.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    # 상품이 주문에 사용된 후 삭제되지 않도록 보호한다.
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # 상품명과 가격을 주문 시점의 값으로 별도 저장한다.
    product_name = models.CharField(max_length=120)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["order", "product"], name="unique_order_product")]

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"

class PaymentRecord(models.Model):
    # 주문마다 하나의 모의 결제 기록만 생성한다.
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="payment")
    # 실제 결제 대행사와 연동하지 않는 교육용 상태이다.
    class Status(models.TextChoices):
        PAID = "paid", "모의 결제 완료"
        REFUNDED = "refunded", "모의 환불 완료"
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PAID)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"주문 {self.order_id} / {self.get_status_display()}"
