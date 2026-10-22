# 연습문제 1~3 정답입니다.
# 실행: uv run python -m exercises.solutions
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from shop.models import Product  # noqa: E402

# 문제 1: 가격이 10만 원보다 싼 상품을 조회하세요.
cheap_products = Product.objects.filter(price__lt=100000)
print("[문제 1] 10만 원 미만 상품")
for product in cheap_products:
    print(product.name, product.price)

# 문제 2: 재고가 있는 상품의 개수를 구하세요.
print("[문제 2] 재고가 있는 상품 수:", Product.objects.filter(stock__gt=0).count())

# 문제 3: 가장 비싼 상품의 이름을 구하세요.
expensive = Product.objects.order_by("-price").first()
print("[문제 3] 최고가 상품:", expensive.name if expensive else "없음")
