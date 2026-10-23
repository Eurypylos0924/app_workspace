"""제17장 프로젝트 상태 점검: DB를 변경하지 않고 필수 구성만 확인한다."""
import os
import sys
from pathlib import Path

# manage.py와 동일한 Django 설정 모듈을 사용한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from django.apps import apps
from django.conf import settings
from django.db import connection


def main():
    """Python 버전·앱 등록·DB 엔진·테이블 상태를 차례로 출력한다."""
    print("Python:", sys.version.split()[0])
    print("Django:", django.get_version())
    print("DB 엔진:", settings.DATABASES["default"]["ENGINE"])
    # DB 비밀번호와 비밀 키는 출력하지 않는다.
    for name in ("shop", "orders", "reports", "accounts", "api"):
        print("앱 등록:", name, apps.is_installed(name))
    # 실제 MySQL 연결이 가능해야 아래 조회가 성공한다.
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE()")
        print("연결 DB:", cursor.fetchone()[0])
    tables = set(connection.introspection.table_names())
    for name in ("shop_product", "shop_category", "orders_order", "orders_orderitem", "orders_paymentrecord"):
        print("테이블:", name, "OK" if name in tables else "MISSING")
    if not all(name in tables for name in ("shop_product", "orders_order", "orders_paymentrecord")):
        raise SystemExit("필수 테이블이 없습니다. 마이그레이션 상태를 확인하세요.")


if __name__ == "__main__":
    main()
