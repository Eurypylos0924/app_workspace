"""Django ORM 모델과 JSON 데이터 간 변환 및 입력 검증을 담당한다."""
from rest_framework import serializers
from shop.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    # 모델에 선언된 필드를 JSON 표현으로 자동 매핑한다.
    class Meta:
        model = Category
        fields = ["id", "name"]
        # DB가 생성하는 기본키는 클라이언트가 수정하지 못한다.
        read_only_fields = ["id"]

class ProductSerializer(serializers.ModelSerializer):
    # 상품 응답에서 분류 이름을 읽기 전용으로 함께 반환한다.
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "category_name", "name", "price", "stock", "description", "created_at"]
        read_only_fields = ["id", "created_at", "category_name"]

    def validate_price(self, value):
        # 상품 가격이 음수라면 HTTP 400 응답으로 입력 오류를 알린다.
        if value < 0:
            raise serializers.ValidationError("가격은 0 이상이어야 한다.")
        return value

    def validate_name(self, value):
        # 공백만 입력한 상품 이름을 허용하지 않는다.
        if not value.strip():
            raise serializers.ValidationError("상품명은 공백일 수 없다.")
        return value.strip()
