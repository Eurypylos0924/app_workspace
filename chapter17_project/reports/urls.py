# 보고서 앱에서 제공하는 URL을 정의한다.
from django.urls import path
from . import views

app_name = "reports"
urlpatterns = [
    # 운영 현황 대시보드 화면이다.
    path("", views.dashboard, name="dashboard"),
    # 주문 데이터를 CSV 파일로 내려받는다.
    path("orders.csv", views.export_orders_csv, name="orders_csv"),
]
