"""프로젝트 최상위 URL: 기능별 앱의 URL 설정을 연결한다."""
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    # /admin/으로 접속하면 Django 관리자 화면을 제공한다.
    path("admin/", admin.site.urls),
    # /accounts/ 하위의 회원가입 URL은 accounts 앱이 관리한다.
    path("accounts/", include("accounts.urls")),
    # 로그인/로그아웃은 Django 기본 인증 뷰를 재사용한다.
    path("accounts/", include("django.contrib.auth.urls")),
    # JSON API는 HTML 페이지와 별도의 /api/ 경로로 제공한다.
    path("api/", include("api.urls")),
    # 관리자 운영 보고서는 /reports/ 경로로 제공한다.
    path("reports/", include("reports.urls")),
    # 주문 화면은 주문 앱에서 독립적으로 처리한다.
    path("", include("orders.urls")),
    # 사이트 루트와 상품 상세 URL은 shop 앱에서 처리한다.
    path("", include("shop.urls")),
]
