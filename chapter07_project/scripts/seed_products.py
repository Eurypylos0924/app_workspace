# Django ORM으로 샘플 상품을 넣는 스크립트입니다.
# 실행: uv run python -m scripts.seed_products
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from shop.models import Product  # noqa: E402  (django.setup() 뒤에 가져와야 합니다)

products = [
    ("노트북", 1200000, 5),
    ("마우스", 25000, 30),
    ("키보드", 65000, 12),
]

for name, price, stock in products:
    # 같은 이름이 있으면 수정하고, 없으면 새로 만듭니다. (여러 번 실행해도 중복되지 않음)
    Product.objects.update_or_create(name=name, defaults={"price": price, "stock": stock})

print(f"현재 상품 수: {Product.objects.count()}")
