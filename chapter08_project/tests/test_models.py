# 모델의 생성/조회/수정/삭제(CRUD)와 PROTECT 동작을 확인하는 테스트입니다.
from decimal import Decimal

import pytest
from django.db.models.deletion import ProtectedError

from shop.models import Category, Product


@pytest.mark.django_db
def test_create_and_read_product():
    category = Category.objects.create(name="문구")
    product = Product.objects.create(
        category=category, name="볼펜",
        price=Decimal("3000.00"), stock=5
    )
    assert Product.objects.get(pk=product.pk).name == "볼펜"


@pytest.mark.django_db
def test_update_and_delete_product():
    category = Category.objects.create(name="문구")
    product = Product.objects.create(
        category=category, name="공책",
        price=Decimal("2000.00"), stock=4
    )
    # 수정: 재고 4 -> 8 (stock 열만 UPDATE)
    product.stock = 8
    product.save(update_fields=["stock"])
    assert Product.objects.get(pk=product.pk).stock == 8

    # 삭제
    product.delete()
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_category_protect():
    category = Category.objects.create(name="문구")
    Product.objects.create(
        category=category, name="연필",
        price=Decimal("5000.00"), stock=2
    )
    # 상품이 있는 카테고리를 지우려 하면 ProtectedError 가 발생해야 합니다.
    with pytest.raises(ProtectedError):
        category.delete()
