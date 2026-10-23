"""운영 통계 화면과 CSV 내보내기 뷰이다."""
import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from orders.models import Order
from .services import get_order_summary, get_status_breakdown


@staff_member_required(login_url="/accounts/login/")
def dashboard(request):
    """관리자(staff)에게만 주문 현황을 보여준다."""
    # 통계 계산을 서비스 함수에 위임한다.
    summary = get_order_summary()
    # 상태별 주문 건수를 함께 표시한다.
    breakdown = get_status_breakdown()
    # 최근 주문 10건만 가져와 불필요한 DB 조회를 제한한다.
    recent_orders = Order.objects.select_related("user").order_by("-created_at", "-id")[:10]
    return render(request, "reports/dashboard.html", {
        "summary": summary,
        "breakdown": breakdown,
        "recent_orders": recent_orders,
    })


@staff_member_required(login_url="/accounts/login/")
def export_orders_csv(request):
    """관리자에게만 주문 요약을 CSV로 제공한다."""
    # Excel에서 한글이 깨지지 않도록 UTF-8 BOM을 기록한다.
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="orders.csv"'
    response.write("\ufeff")
    # csv.writer는 쉼표·따옴표를 자동으로 이스케이프한다.
    writer = csv.writer(response)
    writer.writerow(["주문번호", "사용자", "상태", "총금액", "주문시각"])
    # 사용자를 미리 JOIN하여 주문별 추가 쿼리를 방지한다.
    queryset = Order.objects.select_related("user").order_by("-created_at", "-id")
    for order in queryset.iterator():
        writer.writerow([
            order.pk,
            order.user.get_username(),
            order.status,
            str(order.total_amount),
            order.created_at.isoformat(),
        ])
    return response
