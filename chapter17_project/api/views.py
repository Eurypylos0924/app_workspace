"""상품 및 분류 REST API의 CRUD와 조회 필터를 정의한다."""
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .permissions import ReadOnlyOrStaff
from .serializers import CategorySerializer, ProductSerializer
from shop.models import Category, Product

class CategoryViewSet(viewsets.ModelViewSet):
    # GET 목록/상세, POST 생성, PUT/PATCH 수정, DELETE 삭제를 지원한다.
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrStaff]

class ProductViewSet(viewsets.ModelViewSet):
    # select_related로 분류 이름을 가져올 때 발생하는 N+1 쿼리를 방지한다.
    queryset = Product.objects.select_related("category").all().order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [ReadOnlyOrStaff]

    def get_queryset(self):
        # 목록/상세 조회 모두에 동일한 기본 QuerySet을 적용한다.
        queryset = super().get_queryset()
        # 예: /api/products/?category=1
        category = self.request.query_params.get("category")
        if category is not None:
            if not category.isdecimal():
                raise ValidationError({"category": "분류 ID는 양의 정수여야 한다."})
            queryset = queryset.filter(category_id=int(category))
        # 예: /api/products/?search=노트북
        keyword = self.request.query_params.get("search", "").strip()
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)
        # 클라이언트가 임의의 SQL 정렬 문자열을 지정하지 못하도록 허용 목록을 사용한다.
        ordering = self.request.query_params.get("ordering", "id")
        allowed = {"id", "-id", "name", "-name", "price", "-price", "created_at", "-created_at"}
        if ordering not in allowed:
            raise ValidationError({"ordering": "허용되지 않은 정렬 기준이다."})
        return queryset.order_by(ordering)
