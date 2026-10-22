# 8장 Django ORM · Model · MySQL

Category 1 : N Product 관계를 Django 모델로 만들고, Migration 으로 MySQL 에 반영한 뒤
ORM 으로 CRUD 를 해 보는 실습입니다.

## 환경
- Windows PowerShell, Python 3.12, uv, Django 5.2.7, Docker Desktop
- **8장 전용 MySQL 8.4 컨테이너** (`chapter08-mysql`, 포트 **3308**)
- 7장(`chapter07-mysql`, 포트 3307)과 컨테이너, 포트, 데이터 저장 공간이 모두 분리되어 있습니다.
  두 장 모두 `shop` 앱과 `0001_initial` 마이그레이션을 쓰므로, DB 를 나누지 않으면 마이그레이션이 충돌합니다.

## 실행 순서

### 1. 환경 변수 설정
```powershell
uv sync
Copy-Item .env.example .env
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- `.env` 의 `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD` 를 원하는 값으로 바꿉니다. (7장과 달라도 됩니다)
- 위에서 출력된 키를 `DJANGO_SECRET_KEY` 에 붙여넣습니다.
- `MYSQL_PORT` 는 `3308` 그대로 둡니다.

### 2. 8장 MySQL 컨테이너 실행
```powershell
docker compose config      # 설정 확인 (오류가 없어야 함)
docker compose up -d
docker compose ps          # mysql 이 healthy 가 될 때까지 기다립니다.
```
처음 시작할 때 `sql/00_grant_test_db.sql` 이 자동 실행되어 pytest 용 `test_shopdb` 권한이 부여됩니다.

### 3. 마이그레이션과 실행
```powershell
uv run python manage.py check
uv run python manage.py makemigrations shop --check --dry-run   # 이미 있으면 "No changes detected"
uv run python manage.py migrate
uv run python manage.py showmigrations shop                     # [X] 0001_initial
uv run python -m scripts.seed_products
uv run python manage.py runserver
```
- 목록: http://127.0.0.1:8000/
- 상세: http://127.0.0.1:8000/products/1/
- 없는 상품: http://127.0.0.1:8000/products/999999/ (HTTP 404)

### 4. 관리자 계정
새 DB 라서 관리자 계정을 다시 만들어야 합니다.
```powershell
uv run python manage.py createsuperuser
```
관리자 화면: http://127.0.0.1:8000/admin/

### 5. ORM CRUD 실습
```powershell
uv run python manage.py shell
```
```python
from decimal import Decimal
from shop.models import Category, Product

category, _ = Category.objects.get_or_create(name="도서")
product = Product.objects.create(
    category=category, name="연습용 책",
    price=Decimal("39000.00"), stock=12
)
print(list(Product.objects.filter(category=category, stock__gt=0)))
product.stock = 10
product.save(update_fields=["stock"])
print(Product.objects.get(pk=product.pk).stock)
product.delete()

# 재고 5개 이상 상품을 가격 낮은 순으로
print(list(Product.objects.filter(stock__gte=5).order_by("price")))
# 카테고리에서 거꾸로 상품 조회 (related_name)
print(list(Category.objects.get(name="도서").products.all()))
# 상품이 하나도 없는 카테고리
print(list(Category.objects.filter(products__isnull=True).distinct()))
```

### 6. 테스트
```powershell
uv run pytest -v
```
5개가 통과해야 합니다. pytest 는 별도의 `test_shopdb` 데이터베이스를 만들어 쓰고 끝나면 지웁니다.

### 정리
```powershell
docker compose down        # 컨테이너만 삭제 (데이터는 볼륨에 남음)
# docker compose down -v   # 데이터까지 모두 삭제
```

## 자주 만나는 오류
| 오류 | 원인과 해결 |
|---|---|
| 1045 Access denied | `.env` 비밀번호가 컨테이너를 **처음 만들 때** 값과 다릅니다. 비밀번호를 바꿨다면 `docker compose down -v` 후 다시 `up -d`. |
| 2003 Connection refused | 컨테이너가 꺼져 있거나 `.env` 의 `MYSQL_PORT` 가 3308 이 아닙니다. |
| `port is already allocated` | 3308 을 다른 프로그램이 씁니다. `.env` 의 `MYSQL_PORT` 를 바꾸세요. |
| 1044 Access denied to database 'test_shopdb' | 권한 SQL 이 실행되지 않았습니다. `docker compose down -v` 후 다시 `up -d`. |
| 1146 Table doesn't exist | `migrate` 를 아직 안 했습니다. |

## 주의
- `.env` 는 Git 에 올리지 않습니다.
- `sql/` 의 파일은 MySQL 데이터를 **처음 만들 때 한 번만** 실행됩니다.
