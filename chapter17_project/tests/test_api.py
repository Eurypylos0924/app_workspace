"""pytest-django와 DRF APIClient로 JSON API를 검증한다."""
from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from shop.models import Category, Product

@pytest.fixture
def api_client():
    # 실제 HTTP 서버를 띄우지 않고 Django 요청 처리를 검증한다.
    return APIClient()

@pytest.fixture
def sample_product(db):
    # 테스트 DB에 분류와 상품을 만들고 테스트마다 독립적으로 사용한다.
    category = Category.objects.create(name="전자기기")
    return Product.objects.create(category=category, name="노트북", price=Decimal("1200000.00"), stock=3)

@pytest.mark.django_db
def test_product_list_returns_json(api_client, sample_product):
    # 로그인하지 않아도 목록을 조회할 수 있다.
    response = api_client.get("/api/products/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "노트북"

@pytest.mark.django_db
def test_product_detail_returns_category_name(api_client, sample_product):
    # 분류 이름이 JSON 필드로 반환되는지 검증한다.
    response = api_client.get(f"/api/products/{sample_product.pk}/")
    assert response.status_code == 200
    assert response.data["category_name"] == "전자기기"

@pytest.mark.django_db
def test_anonymous_cannot_create_product(api_client, sample_product):
    # 비로그인 사용자의 데이터 변경 요청은 거부되어야 한다.
    data = {"category": sample_product.category_id, "name": "마우스", "price": "15000.00", "stock": 5}
    response = api_client.post("/api/products/", data, format="json")
    assert response.status_code in (401, 403)

@pytest.mark.django_db
def test_staff_can_create_product(api_client, sample_product):
    # 관리자 권한 사용자에게만 POST를 허용한다.
    user = get_user_model().objects.create_user(username="staff", password="safe-test-pass-123", is_staff=True)
    api_client.force_authenticate(user=user)
    data = {"category": sample_product.category_id, "name": "마우스", "price": "15000.00", "stock": 5}
    response = api_client.post("/api/products/", data, format="json")
    assert response.status_code == 201
    assert Product.objects.filter(name="마우스").exists()

@pytest.mark.django_db
def test_negative_price_is_rejected(api_client, sample_product):
    # Serializer의 validate_price()가 잘못된 입력을 막는지 확인한다.
    user = get_user_model().objects.create_user(username="manager", password="safe-test-pass-123", is_staff=True)
    api_client.force_authenticate(user=user)
    data = {"category": sample_product.category_id, "name": "오류상품", "price": "-1", "stock": 1}
    response = api_client.post("/api/products/", data, format="json")
    assert response.status_code == 400
    assert "price" in response.data

@pytest.mark.django_db
def test_search_and_invalid_ordering(api_client, sample_product):
    # 검색어 필터와 잘못된 정렬 인수의 오류 처리를 검증한다.
    assert api_client.get("/api/products/?search=노트").data["count"] == 1
    assert api_client.get("/api/products/?ordering=invalid").status_code == 400
