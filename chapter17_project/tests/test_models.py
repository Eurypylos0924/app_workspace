"""pytest-django로 MySQL 테스트 DB에서 ORM 동작을 검증한다."""
from decimal import Decimal
import pytest
from django.db.models import ProtectedError
from shop.models import Category, Product

@pytest.mark.django_db
def test_product_create_and_read():
    # 테스트 데이터베이스에 분류를 생성한다.
    category = Category.objects.create(name="노트북")
    # 외래키를 연결하여 상품을 생성한다.
    product = Product.objects.create(category=category, name="실습용 노트북", price=Decimal("950000.00"), stock=3)
    # 실제 데이터베이스에서 다시 조회한 값을 확인한다.
    saved = Product.objects.get(pk=product.pk)
    assert saved.name == "실습용 노트북"
    assert saved.category.name == "노트북"
    assert saved.price == Decimal("950000.00")

@pytest.mark.django_db
def test_product_update_and_delete():
    category = Category.objects.create(name="주변기기")
    product = Product.objects.create(category=category, name="마우스", price=Decimal("15000.00"))
    # UPDATE를 실행하고 변경 내용을 재조회한다.
    product.stock = 8
    product.save(update_fields=["stock"])
    assert Product.objects.get(pk=product.pk).stock == 8
    # DELETE를 실행한 뒤 상품이 사라졌는지 확인한다.
    product.delete()
    assert not Product.objects.filter(pk=product.pk).exists()

@pytest.mark.django_db
def test_category_protect():
    category = Category.objects.create(name="모니터")
    Product.objects.create(category=category, name="27인치", price=Decimal("200000.00"))
    # 상품이 연결된 분류는 PROTECT 정책에 따라 삭제할 수 없다.
    with pytest.raises(ProtectedError):
        category.delete()
