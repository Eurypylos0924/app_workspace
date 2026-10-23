"""쇼핑몰 실습용 상품 초기 데이터 등록."""


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


from decimal import Decimal
from django.db import transaction
from shop.models import Category, Product

# (분류명, 상품명, 가격, 재고, 설명)
SAMPLE_PRODUCTS = [
    ("전자기기", "무선 키보드", "39000", 12, "블루투스 무선 키보드"),
    ("전자기기", "무선 마우스", "25000", 20, "인체공학 무선 마우스"),
    ("전자기기", "USB-C 허브", "45000", 15, "멀티포트 USB-C 허브"),
    ("전자기기", "27인치 모니터", "249000", 7, "QHD 업무용 모니터"),
    ("전자기기", "노트북 거치대", "32000", 18, "높이 조절 알루미늄 거치대"),
    ("생활용품", "스테인리스 텀블러", "18000", 30, "보온 보냉 텀블러"),
    ("생활용품", "탁상용 LED 조명", "29000", 14, "밝기 조절 LED 조명"),
    ("생활용품", "수납 정리함", "16000", 25, "다용도 책상 정리함"),
    ("생활용품", "에코백", "12000", 40, "면 소재 장바구니"),
    ("생활용품", "미니 가습기", "35000", 11, "USB 전원 가습기"),
    ("도서", "파이썬 프로그래밍 입문", "28000", 22, "Python 기초 학습 도서"),
    ("도서", "Django 웹 개발", "33000", 16, "Django 웹 서비스 실습"),
    ("도서", "데이터 분석 기초", "31000", 13, "Pandas 데이터 분석"),
    ("도서", "머신러닝 입문", "36000", 9, "머신러닝 개념과 실습"),
    ("도서", "SQL 실무 가이드", "27000", 19, "관계형 데이터베이스 활용"),
    ("사무용품", "A5 노트", "4500", 50, "줄노트 100매"),
    ("사무용품", "볼펜 세트", "6900", 60, "검정 파랑 빨강 볼펜"),
    ("사무용품", "파일 홀더", "8500", 35, "문서 정리용 파일 홀더"),
    ("사무용품", "데스크 매트", "22000", 21, "미끄럼 방지 데스크 매트"),
    ("사무용품", "포스트잇 세트", "5900", 45, "메모지 5종 세트"),
]

# 기존 상품의 가격·재고·설명을 덮어쓰지 않는다.
with transaction.atomic():
    created_count = 0
    for category_name, name, price, stock, description in SAMPLE_PRODUCTS:
        category, _ = Category.objects.get_or_create(name=category_name)
        _, created = Product.objects.get_or_create(
            category=category,
            name=name,
            defaults={
                "price": Decimal(price),
                "stock": stock,
                "description": description,
            },
        )
        created_count += int(created)

print(f"새로 등록한 상품: {created_count}개")
print(f"전체 분류: {Category.objects.count()}개")
print(f"전체 상품: {Product.objects.count()}개")
