# 7장 ORM 모델: MySQL의 shop_product 테이블과 연결됩니다.
from django.db import models


class Product(models.Model):
    # 상품 이름
    name = models.CharField(max_length=100)
    # 가격과 재고는 음수가 될 수 없으므로 PositiveIntegerField를 씁니다.
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        # 기본 정렬: Product.objects.all() 결과를 id 오름차순으로 돌려줍니다.
        # order_by()를 따로 쓰지 않아도 항상 같은 순서가 보장됩니다.
        ordering = ["id"]

        # id 내림차순(최신순)으로 보고 싶다면 아래처럼 바꿉니다.
        # ordering = ["-id"]

    def __str__(self):
        return self.name
