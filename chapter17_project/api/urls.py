"""DRF Router가 ViewSet 메서드와 URL을 자동 연결한다."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

# basename은 URL 이름을 생성하는 데 사용된다.
router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")

urlpatterns = [
    # /api/products/, /api/products/1/ 등의 URL을 자동 생성한다.
    path("", include(router.urls)),
    # DRF의 Browsable API에서 세션 로그인/로그아웃 기능을 제공한다.
    path("auth/", include("rest_framework.urls")),
]
