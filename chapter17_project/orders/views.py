from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from shop.cart import build_cart_context
from .models import Order
from .services import create_order_from_cart, cancel_order, confirm_order

@login_required
def checkout(request):
    # GET 요청에서는 주문 전 상품과 합계를 다시 보여준다.
    if request.method == "GET":
        return render(request, "orders/checkout.html", build_cart_context(request))
    # 재고 차감과 주문 저장은 POST 요청에서만 허용한다.
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])
    try:
        order = create_order_from_cart(request)
    except ValidationError as exc:
        # 검증 오류가 발생해도 재고와 주문 정보는 변경하지 않는다.
        messages.error(request, "; ".join(exc.messages))
        return redirect("checkout")
    messages.success(request, "주문이 접수되었습니다. 실제 결제는 수행하지 않습니다.")
    return redirect("order_detail", pk=order.pk)

@login_required
def order_list(request):
    # 다른 사용자의 주문은 절대로 조회하지 않는다.
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders/order_list.html", {"orders": orders})

@login_required
def order_detail(request, pk):
    # 소유자 조건을 쿼리에 포함해 타인의 주문 접근을 차단한다.
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=pk, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


from django.views.decorators.http import require_POST

@login_required
@require_POST
def order_cancel(request, pk):
    # 상태 변경은 GET이 아니라 CSRF 보호를 받는 POST에서만 수행한다.
    try:
        cancel_order(pk, request.user)
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    else:
        messages.success(request, "주문을 취소하고 상품 재고를 복원했습니다.")
    return redirect("order_detail", pk=pk)

@login_required
@require_POST
def order_confirm(request, pk):
    # 일반 사용자의 확인 요청은 명시적으로 거부한다.
    from django.http import HttpResponseForbidden
    if not request.user.is_staff:
        return HttpResponseForbidden("관리자 권한이 필요합니다.")
    try:
        confirm_order(pk, request.user)
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    else:
        messages.success(request, "주문을 확인 처리했습니다.")
    return redirect("order_detail", pk=pk)


from .payment_services import simulate_payment, simulate_refund

@login_required
@require_POST
def order_pay(request, pk):
    # POST와 로그인 검사로 비인가 결제 시도를 차단한다.
    try:
        simulate_payment(pk, request.user)
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    else:
        messages.success(request, "교육용 모의 결제가 완료되었습니다. 실제 금액은 청구되지 않습니다.")
    return redirect("order_detail", pk=pk)

@login_required
@require_POST
def order_refund(request, pk):
    # 기존 주문 취소 이후 모의 결제 기록만 환불 상태로 바꾼다.
    try:
        simulate_refund(pk, request.user)
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    else:
        messages.success(request, "모의 환불 기록이 완료되었습니다.")
    return redirect("order_detail", pk=pk)
