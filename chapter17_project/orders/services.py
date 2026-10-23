from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from shop.cart import get_cart, parse_quantity, CART_SESSION_KEY
from shop.models import Product
from .models import Order, OrderItem

@transaction.atomic
def create_order_from_cart(request):
    """장바구니를 주문으로 저장하고 상품 재고를 원자적으로 차감한다."""
    # 장바구니는 서버의 세션에 저장되며 상품 가격은 반드시 DB에서 다시 읽는다.
    cart = get_cart(request)
    if not cart:
        raise ValidationError("장바구니가 비어 있습니다.")
    # 세션에 상품 ID 이외의 값이 들어 있으면 잘못된 요청으로 처리한다.
    if any(not str(key).isdecimal() for key in cart):
        raise ValidationError("장바구니 상품 ID가 올바르지 않습니다.")
    product_ids = sorted(int(key) for key in cart)
    # select_for_update()는 MySQL InnoDB에서 해당 상품 행을 잠가 동시 주문을 보호한다.
    products = list(Product.objects.select_for_update().filter(pk__in=product_ids).order_by("pk"))
    if len(products) != len(product_ids):
        raise ValidationError("판매하지 않는 상품이 포함되어 있습니다.")
    lines = []
    total = Decimal("0.00")
    for product in products:
        # 수량은 숫자와 범위를 검증하고 현재 재고를 다시 확인한다.
        quantity = parse_quantity(cart[str(product.pk)])
        if quantity > product.stock:
            raise ValidationError(f"{product.name}의 재고가 부족합니다.")
        subtotal = product.price * quantity
        lines.append((product, quantity, subtotal))
        total += subtotal
    # 모든 항목을 검증한 뒤 주문과 주문 항목을 생성한다.
    order = Order.objects.create(user=request.user, total_amount=total)
    for product, quantity, subtotal in lines:
        OrderItem.objects.create(
            order=order, product=product, product_name=product.name,
            unit_price=product.price, quantity=quantity, subtotal=subtotal,
        )
        # 동일한 트랜잭션에서 재고를 차감한다. 중간에 실패하면 전체가 롤백된다.
        product.stock -= quantity
        product.save(update_fields=["stock"])
    # DB 저장이 확정된 뒤에만 세션의 장바구니를 비운다.
    transaction.on_commit(lambda: clear_cart_after_commit(request))
    return order

def clear_cart_after_commit(request):
    # 트랜잭션이 커밋되면 브라우저의 세션 장바구니를 초기화한다.
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True


@transaction.atomic
def cancel_order(order_id, user):
    """주문 소유권·상태를 검증한 뒤 재고를 한 번만 복원한다."""
    # 주문 행을 잠가 동시에 두 번 취소되는 상황을 차단한다.
    order = Order.objects.select_for_update().filter(pk=order_id, user=user).first()
    if order is None:
        raise ValidationError("주문을 찾을 수 없습니다.")
    # 접수 상태의 주문만 취소할 수 있다. 이미 취소한 주문은 재고를 복원하지 않는다.
    if order.status != Order.Status.PENDING:
        raise ValidationError("접수 상태의 주문만 취소할 수 있습니다.")
    # 상품 잠금 순서를 일정하게 유지하여 동시 요청의 교착 가능성을 낮춘다.
    items = list(order.items.select_related("product").order_by("product_id"))
    product_ids = [item.product_id for item in items]
    locked_products = {
        p.pk: p for p in Product.objects.select_for_update().filter(pk__in=product_ids).order_by("pk")
    }
    # 주문 시 보호(PROTECT)된 상품은 삭제되지 않아야 한다.
    if len(locked_products) != len(set(product_ids)):
        raise ValidationError("주문 상품 정보가 일치하지 않습니다.")
    # 원래 주문한 수량만큼만 재고를 되돌린다.
    for item in items:
        product = locked_products[item.product_id]
        product.stock += item.quantity
        product.save(update_fields=["stock"])
    # 재고 복원과 상태 변경은 동일한 트랜잭션에서 확정된다.
    from django.utils import timezone
    order.status = Order.Status.CANCELLED
    order.cancelled_at = timezone.now()
    order.save(update_fields=["status", "cancelled_at"])
    return order

@transaction.atomic
def confirm_order(order_id, staff_user):
    """관리자만 접수 주문을 확인 상태로 변경한다."""
    if not staff_user.is_staff:
        raise ValidationError("관리자만 주문을 확인할 수 있습니다.")
    order = Order.objects.select_for_update().filter(pk=order_id).first()
    if order is None or order.status != Order.Status.PENDING:
        raise ValidationError("접수 상태의 주문을 찾을 수 없습니다.")
    order.status = Order.Status.CONFIRMED
    order.save(update_fields=["status"])
    return order
