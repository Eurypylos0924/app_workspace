"""제11장 검색·필터·정렬·페이지네이션 자동 테스트."""
from decimal import Decimal
import pytest
from django.urls import reverse
from shop.models import Category, Product

@pytest.fixture
def products(db):
    # 실제 서비스 데이터 대신 pytest 전용 임시 MySQL 테스트 DB에 샘플을 만든다.
    category = Category.objects.create(name="전자기기")
    other = Category.objects.create(name="문구")
    Product.objects.create(category=category, name="노트북", description="가벼운 컴퓨터", price=Decimal("1200000"), stock=5)
    Product.objects.create(category=category, name="마우스", description="무선 입력기기", price=Decimal("25000"), stock=9)
    Product.objects.create(category=other, name="연필", description="필기용", price=Decimal("1000"), stock=10)
    return category

def test_keyword_search(client, products):
    # 상품명 부분 일치 검색을 확인한다.
    response = client.get(reverse("product_list"), {"q": "노트"})
    assert response.status_code == 200
    assert [p.name for p in response.context["products"]] == ["노트북"]

def test_category_filter(client, products):
    # 카테고리 외래키를 기준으로 두 상품만 조회되는지 확인한다.
    response = client.get(reverse("product_list"), {"category": products.pk})
    assert response.context["page_obj"].paginator.count == 2

def test_price_filter(client, products):
    # 최소·최대 가격을 동시에 적용한다.
    response = client.get(reverse("product_list"), {"min_price": "20000", "max_price": "30000"})
    assert [p.name for p in response.context["products"]] == ["마우스"]

def test_sort_price(client, products):
    # 가격 오름차순 결과를 확인한다.
    response = client.get(reverse("product_list"), {"sort": "price_asc"})
    assert [p.name for p in response.context["products"]] == ["연필", "마우스", "노트북"]

def test_invalid_category_is_empty(client, products):
    # 숫자가 아닌 카테고리 ID를 전달해도 서버 오류 없이 빈 목록을 반환한다.
    response = client.get(reverse("product_list"), {"category": "invalid"})
    assert response.status_code == 200
    assert response.context["page_obj"].paginator.count == 0

def test_detail_missing_returns_404(client, products):
    # 존재하지 않는 상품은 HTTP 404를 반환해야 한다.
    response = client.get(reverse("product_detail", args=[999999]))
    assert response.status_code == 404
