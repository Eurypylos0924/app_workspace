# 7장 Docker · MySQL 설치 및 SQL 기초

## 환경
- Windows PowerShell, Python 3.12, uv, Docker Desktop (Linux 컨테이너)
- MySQL 8.4 컨테이너, Django 5.2.7, mysqlclient, pytest, pytest-django

## 실행 방법
```powershell
uv sync
Copy-Item .env.example .env
# .env 를 열어 MySQL 비밀번호와 Django 키를 바꿉니다.
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# 출력된 값을 .env 의 DJANGO_SECRET_KEY 에 붙여넣습니다.
docker compose up -d
# docker compose ps 에서 mysql 이 healthy 가 될 때까지 기다립니다.
docker compose ps
uv run python manage.py migrate
uv run python -m scripts.seed_products
uv run python manage.py runserver 127.0.0.1:8000
```
접속: http://127.0.0.1:8000/

## SQL 실습
```powershell
# 실행 중인 MySQL 컨테이너에 접속합니다.
docker compose exec mysql sh -c 'MYSQL_PWD="$MYSQL_PASSWORD" mysql -u"$MYSQL_USER" "$MYSQL_DATABASE"'
# 접속 후 mysql> 에서 sql/03_queries.sql 의 문장을 한 줄씩 실행해 봅니다.
```

## 테스트
```powershell
# MySQL 컨테이너가 켜져 있어야 합니다.
# pytest는 별도의 테스트 DB(test_shopdb)를 만들어 쓰고 끝나면 지웁니다.
uv run pytest -v
uv run python -m exercises.solutions
```

## 정리
```powershell
docker compose down
# 데이터까지 모두 지우려면 아래 명령을 씁니다.
# docker compose down -v
```

참고: sql/01_schema.sql 과 02_seed.sql 은 MySQL 데이터가 처음 만들어질 때만 실행됩니다.
주의: `.env` 는 Git에 올리지 않습니다. 운영 환경에서는 DEBUG=False, ALLOWED_HOSTS 를 반드시 점검하세요.
