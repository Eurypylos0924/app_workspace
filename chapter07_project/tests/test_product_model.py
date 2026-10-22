# Django ORM과 MySQL이 잘 동작하는지 확인하는 모델 테스트입니다.
import pytest

from shop.models import Product


@pytest.mark.django_db
def test_create_product():
    # 상품을 하나 만들고 DB에서 다시 읽어옵니다.
    product = Product.objects.create(name="모니터", price=220000, stock=8)
    # 저장한 값이 그대로 조회되는지 확인합니다.
    assert Product.objects.get(pk=product.pk).name == "모니터"
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_product_ordering():
    # 기본 정렬(id 오름차순)대로 나오는지 확인합니다.
    Product.objects.create(name="키보드", price=65000, stock=3)
    Product.objects.create(name="마우스", price=25000, stock=4)
    assert list(Product.objects.values_list("name", flat=True)) == ["키보드", "마우스"]
