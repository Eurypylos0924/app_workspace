
"""MySQL에 카테고리와 예제 상품 데이터를 등록하거나 수정한다."""

import os
import sys
from pathlib import Path
from decimal import Decimal

# 프로젝트 루트 경로를 구한다.
BASE_DIR = Path(__file__).resolve().parent.parent

# 프로젝트 루트를 Python 모듈 검색 경로에 추가한다.
sys.path.insert(0, str(BASE_DIR))

# Django 설정 모듈을 지정한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Django 환경을 초기화한다.
import django
django.setup()

# Django 초기화 이후 모델을 가져온다.
from shop.models import Category, Product

# 카테고리별 상품 데이터를 정의한다.
# 상품 데이터는 (상품명, 가격, 재고) 순서로 구성한다.
product_data = {
    "전자기기": [
        ("무선 키보드", "39000.00", 12),
        ("무선 마우스", "19000.00", 7),
        ("노트북", "1250000.00", 5),
        ("모니터", "289000.00", 8),
        ("USB 허브", "25000.00", 20),
    ],
    "생활가전": [
        ("공기청정기", "320000.00", 6),
        ("로봇청소기", "590000.00", 4),
        ("전기히터", "89000.00", 15),
        ("가습기", "65000.00", 11),
        ("선풍기", "79000.00", 9),
    ],
    "사무용품": [
        ("A4 복사용지", "6500.00", 100),
        ("볼펜 세트", "12000.00", 50),
        ("파일 바인더", "4500.00", 40),
        ("메모지", "3500.00", 80),
        ("책상 정리함", "18000.00", 25),
    ],
    "주방용품": [
        ("프라이팬", "35000.00", 15),
        ("냄비 세트", "89000.00", 10),
        ("전기포트", "45000.00", 18),
        ("텀블러", "25000.00", 30),
        ("도마 세트", "19000.00", 22),
    ],
    "생활용품": [
        ("수건 세트", "29000.00", 35),
        ("세탁세제", "18000.00", 40),
        ("휴지 30롤", "22000.00", 45),
        ("욕실 슬리퍼", "9000.00", 28),
        ("청소용 밀대", "32000.00", 16),
    ],
    "스포츠용품": [
        ("요가 매트", "29000.00", 20),
        ("덤벨 세트", "65000.00", 12),
        ("운동용 장갑", "15000.00", 30),
        ("줄넘기", "12000.00", 25),
        ("폼롤러", "25000.00", 18),
    ],
}

# 새로 생성된 카테고리와 상품 수를 기록한다.
created_categories = 0
created_products = 0
updated_products = 0

# 카테고리별 상품을 등록한다.
for category_name, products in product_data.items():

    # 카테고리가 없으면 생성하고, 있으면 기존 객체를 가져온다.
    category, category_created = Category.objects.get_or_create(
        name=category_name
    )

    # 새로 생성된 카테고리 수를 증가시킨다.
    if category_created:
        created_categories += 1

    print(f"\n[카테고리] {category_name}")

    # 해당 카테고리의 상품을 순서대로 처리한다.
    for name, price, stock in products:

        # 상품이 존재하면 수정하고, 없으면 생성한다.
        product, product_created = Product.objects.update_or_create(
            category=category,
            name=name,
            defaults={
                "price": Decimal(price),
                "stock": stock,
            },
        )

        # 생성 여부에 따라 처리 결과를 기록한다.
        if product_created:
            created_products += 1
            status = "신규 등록"
        else:
            updated_products += 1
            status = "기존 수정"

        # 처리한 상품 정보를 출력한다.
        print(
            f"  {status}: {product.name} / "
            f"{product.price:,.0f}원 / "
            f"재고 {product.stock}개"
        )

# 전체 처리 결과를 출력한다.
print("\n========== 상품 데이터 처리 결과 ==========")
print(f"신규 카테고리: {created_categories}개")
print(f"신규 상품: {created_products}개")
print(f"수정 상품: {updated_products}개")
print(f"전체 카테고리: {Category.objects.count()}개")
print(f"전체 상품: {Product.objects.count()}개")

# 카테고리별 등록된 상품 개수를 출력한다.
print("\n========== 카테고리별 상품 현황 ==========")

for category in Category.objects.all().order_by("id"):
    count = Product.objects.filter(category=category).count()
    print(f"{category.name}: {count}개")
