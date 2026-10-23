"""ORM 모델: Category(1)와 Product(N)의 관계를 정의한다."""
from django.db import models

class Category(models.Model):
    # 분류 이름은 중복 등록하지 않는다.
    name = models.CharField("분류명", max_length=80, unique=True)

    class Meta:
        # 기본 테이블명은 shop_category이다.
        ordering = ["name"]
        verbose_name = "상품 분류"
        verbose_name_plural = "상품 분류"

    def __str__(self):
        # 관리자 화면에 분류 이름을 표시한다.
        return self.name

class Product(models.Model):
    # ForeignKey는 MySQL의 category_id 컬럼으로 저장된다.
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # 연결된 상품이 있으면 분류 삭제를 막는다.
        related_name="products",  # category.products.all() 역참조를 허용한다.
        verbose_name="상품 분류",
    )
    name = models.CharField("상품명", max_length=120)
    # 금액은 부동소수점 오차 방지를 위해 DecimalField로 저장한다.
    price = models.DecimalField("가격", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("재고", default=0)
    description = models.TextField("설명", blank=True)
    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        # 기본 테이블명은 shop_product이다.
        ordering = ["id"]
        verbose_name = "상품"
        verbose_name_plural = "상품"

    def __str__(self):
        return self.name
