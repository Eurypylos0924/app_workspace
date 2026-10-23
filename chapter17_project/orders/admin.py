from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    # 주문 상세 화면에서 품목을 읽기 전용으로 보여준다.
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("product", "product_name", "unit_price", "quantity", "subtotal")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "created_at")
    list_select_related = ("user",)
    readonly_fields = ("user", "total_amount", "created_at")
    inlines = [OrderItemInline]
    def has_add_permission(self, request):
        # 주문은 장바구니 검증 서비스를 통해서만 생성한다.
        return False


from .models import PaymentRecord

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    # 모의 결제 기록은 관리자에서 조회 전용으로 제공한다.
    list_display = ("order", "status", "amount", "paid_at", "refunded_at")
    readonly_fields = ("order", "status", "amount", "paid_at", "refunded_at")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
