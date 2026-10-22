# 8장 모델: Category 1 : N Product 관계를 만듭니다.
from django.db import models


class Category(models.Model):
    # 카테고리 이름 (중복 불가)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # 상품이 속한 카테고리 (외래키)
    # on_delete=PROTECT: 상품이 있는 카테고리는 삭제할 수 없습니다.
    # related_name="products": category.products.all() 로 거꾸로 조회할 수 있습니다.
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    # 금액은 오차 없는 DecimalField 로 저장합니다.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
