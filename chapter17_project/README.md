# 제17장 Django 쇼핑몰 통합 테스트·최종 검증

제16장의 기능을 포함한 **독립 실행 Django 쇼핑몰 프로젝트**이다. 상품 조회·검색, 장바구니, 주문, 모의 결제·취소·환불, 보고서, API 및 통합 테스트를 다룬다. **실제 PG사 결제는 수행하지 않는다.**

## 1. 개발 환경 및 실행 전 점검

| 구성 요소 | 기준 |
|---|---|
| 운영체제 / 터미널 | Windows / PowerShell |
| Python | 3.12.x |
| 패키지 관리자 | uv (`uv.lock` 사용) |
| 웹 프레임워크 | Django 5.2.7 |
| 데이터베이스 | Docker Desktop + MySQL 8.4 (InnoDB) |
| 테스트 | pytest, pytest-django |
| 데이터베이스 접속 | Windows `127.0.0.1:3308` → 컨테이너 `3306` (권장 예시) |

> **포트 주의:** 첨부 프로젝트의 `compose.yaml`은 `${MYSQL_PORT:-3308}`을 사용하지만 원본 `.env.example`은 `MYSQL_PORT=3307`, `DB_PORT=3307`로 되어 있다. 이 문서는 다른 장의 MySQL과 충돌하지 않도록 **3308**로 통일하는 예시이다. 이미 3307로 정상 운영 중이라면 임의로 바꾸지 말고 `MYSQL_PORT`와 `DB_PORT`를 같은 값으로 유지한다.

Docker Desktop을 실행하고 `docker version`, `uv --version`, `Get-Location`을 확인한다. PowerShell 명령어는 별도 표시가 없는 한 **프로젝트 루트 `C:\lab\chapter17_project`에서 실행**한다.

## 2. 프로젝트 폴더 확인

```text
chapter17_project/
├── .env.example           # 환경변수 예시
├── .env                   # 로컬 비밀번호·비밀키 (Git에 올리지 않음)
├── compose.yaml           # MySQL 8.4 서비스와 볼륨
├── pyproject.toml         # Python 패키지 및 pytest 설정
├── uv.lock                # 패키지 잠금 파일
├── manage.py
├── config/                # Django 설정 및 URL
├── accounts/              # 사용자 관련 기능
├── shop/                  # 분류·상품·장바구니
├── orders/                # 주문·결제·환불
├── reports/               # 보고서
├── api/                   # REST API
├── scripts/
│   ├── seed_products.py   # 예제 상품 등록
│   └── verify_project.py  # 실행 환경·DB 테이블 점검
└── tests/
    └── test_integration_flow.py  # 통합 테스트
```

## 3. 작업 순서 ① Python·uv 준비

```powershell
Set-Location C:\lab\chapter17_project
uv python install 3.12
uv sync --dev
uv run python --version
uv run python -m django --version
```

`uv sync --dev`는 `pyproject.toml`과 `uv.lock`을 기준으로 `.venv`를 구성하고 개발 의존성인 pytest를 설치한다. `uv`가 없다면 PowerShell에서 공식 설치 스크립트 `irm https://astral.sh/uv/install.ps1 | iex`를 실행한 뒤 새 터미널을 연다.

**확인 기준:** Python 3.12.x, Django 5.2.7이 표시된다.

## 4. 작업 순서 ② `.env` 생성 및 설정

최초 설치 시에만 `.env.example`을 복사한다. **이미 `.env`가 존재하면 덮어쓰지 않는다.**

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

권장 설정 예시(실제 비밀번호·비밀키로 교체):

```dotenv
MYSQL_DATABASE=shopdb
MYSQL_USER=shopuser
MYSQL_PASSWORD=본인이_설정한_앱_비밀번호
MYSQL_ROOT_PASSWORD=본인이_설정한_root_비밀번호
MYSQL_PORT=3308
DB_NAME=shopdb
DB_USER=shopuser
DB_PASSWORD=본인이_설정한_앱_비밀번호
DB_HOST=127.0.0.1
DB_PORT=3308
DJANGO_SECRET_KEY=실제로_생성한_긴_비밀키
DJANGO_DEBUG=True
```

Django용 `DB_PASSWORD`와 컨테이너 최초 생성용 `MYSQL_PASSWORD`는 동일하게 지정한다. Django용 `DB_PORT`와 Docker의 호스트 포트 `MYSQL_PORT`도 동일해야 한다. `DB_HOST`에 포트 번호를 입력하지 않는다.

비밀키 생성:

```powershell
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

출력된 문자열을 `.env`의 `DJANGO_SECRET_KEY`에 붙여넣는다. `.env`는 외부에 공유하지 않는다.

> **기존 볼륨 주의:** MySQL 컨테이너가 이미 초기화되었다면 `.env`의 `MYSQL_PASSWORD` 또는 `MYSQL_ROOT_PASSWORD`를 수정해도 **기존 MySQL 계정 비밀번호가 자동으로 바뀌지 않는다**. 인증 오류가 발생하면 실제 MySQL 계정의 비밀번호와 일치하는지 확인한다.

## 5. 작업 순서 ③ Docker MySQL 실행

```powershell
docker compose config
docker compose up -d
docker compose ps
docker ps -a
Test-NetConnection 127.0.0.1 -Port 3308
```

`docker compose ps`에서 `chapter17-mysql`이 `Up (healthy)` 상태인지 확인한다. `Test-NetConnection` 결과가 `TcpTestSucceeded : True`이면 포트 연결이 가능한 상태이다. **이는 MySQL 사용자 인증 성공을 보장하지 않는다.**

컨테이너 내부의 MySQL에 접속할 때는 호스트 포트 매핑을 지정하지 않는다.

```powershell
# 일반 사용자 접속
 docker exec -it chapter17-mysql mysql -u shopuser -p shopdb
# 관리자 접속 (필요할 때만)
 docker exec -it chapter17-mysql mysql -u root -p
```

MySQL 프롬프트에서는 SQL을 입력한다.

```sql
SELECT DATABASE();
SHOW TABLES;
EXIT;
```

**주의:** `3308:3306`은 `compose.yaml`의 `ports`에 쓰는 형식이다. `docker exec ... mysql -P 3308:3306`처럼 입력하지 않는다. `docker exec`는 컨테이너 내부에서 실행되므로 기본 MySQL 포트 `3306`을 사용한다.

## 6. 작업 순서 ④ Django 설정 및 마이그레이션

```powershell
uv run python manage.py check
uv run python manage.py showmigrations shop orders
uv run python manage.py migrate
uv run python manage.py showmigrations shop orders
```

마이그레이션 후 `[X]`가 적용 완료를 의미한다. 필수 테이블은 `shop_category`, `shop_product`, `orders_order`, `orders_orderitem`, `orders_paymentrecord`이다.

테이블 목록 확인:

```powershell
uv run python manage.py shell -c "from django.db import connection; print(connection.introspection.table_names())"
```

`Table 'shopdb.shop_product' doesn't exist`가 나타나면 DB 이름과 마이그레이션 적용 여부를 먼저 확인한다. `--fake`로 임의 처리하거나 기존 DB 테이블을 삭제하지 않는다.

## 7. 작업 순서 ⑤ 예제 상품 데이터 등록

**중요:** 첨부 프로젝트의 `scripts/seed_products.py`는 최상위에서 Django 모델을 import하므로, 원본 그대로 `uv run python -m scripts.seed_products`를 실행하면 Django 초기화 오류가 발생할 수 있다. 다음처럼 Django 셸에서 실행한다.

```powershell
uv run python manage.py shell -c "exec(open('scripts/seed_products.py', encoding='utf-8').read())"
uv run python manage.py shell -c "from shop.models import Category, Product; print('분류:', Category.objects.count(), '상품:', Product.objects.count())"
```

원본 `seed_products.py`는 **전자기기 분류와 무선 키보드 상품 1개**를 `get_or_create()`로 등록한다. 상품 20개 버전의 스크립트로 교체한 경우에는 해당 스크립트의 등록 수에 따른다. 중복 실행 시 기존 상품을 재사용하므로 무조건 새 상품이 늘어나지는 않는다.

## 8. 작업 순서 ⑥ 프로젝트 구성 검증

```powershell
uv run python -m scripts.verify_project
```

Python·Django 버전, `shop`·`orders`·`reports`·`accounts`·`api` 앱 등록, MySQL 연결 DB 이름, 필수 테이블 존재 여부를 출력한다. 필수 테이블이 누락되면 검증이 실패한다.

## 9. 작업 순서 ⑦ pytest용 MySQL 권한 확인

pytest-django는 기본적으로 개발 DB `shopdb`와 별도의 **`test_shopdb`**를 생성한다. 데이터베이스 생성 권한이 없다면 `SystemExit: 2`가 나타날 수 있다. 실제 MySQL 오류 메시지를 확인한 뒤 권한을 수정한다.

관리자 계정으로 접속(명령어는 **PowerShell**에서 실행):

```powershell
docker exec -it chapter17-mysql mysql -u root -p
```

계정과 권한 확인(아래 명령어는 **MySQL 프롬프트**에서 실행):

```sql
SELECT user, host FROM mysql.user WHERE user = 'shopuser';
SHOW GRANTS FOR 'shopuser'@'%';
```

`'shopuser'@'%'`가 실제로 존재하고 테스트 DB 생성 권한이 부족한 것으로 확인된 **로컬 실습 환경**에서만 관리자 계정으로 다음을 실행한다.

```sql
GRANT CREATE ON *.* TO 'shopuser'@'%';
GRANT ALL PRIVILEGES ON `test_shopdb`.* TO 'shopuser'@'%';
SHOW GRANTS FOR 'shopuser'@'%';
EXIT;
```

`CREATE ON *.*`는 광범위한 생성 권한이다. 운영 환경에서는 전용 테스트 계정 또는 별도의 테스트 DB 서버를 사용한다. `shopuser`의 실제 호스트가 `%`가 아니면 계정 호스트를 확인한 후 적절하게 변경해야 한다.

## 10. 작업 순서 ⑧ 통합 테스트 실행

MySQL 콘솔을 종료한 뒤 **PowerShell**에서 실행한다.

```powershell
# 핵심 통합 테스트
uv run python -m pytest tests/test_integration_flow.py -v

# 전체 테스트
uv run python -m pytest -v
```

문제가 생기면 최초 예외의 전체 traceback을 확인한다.

```powershell
uv run python -m pytest tests/test_integration_flow.py -vv -s --tb=long -x
```

`-vv`는 상세 출력, `-s`는 출력 캡처 해제, `--tb=long`은 상세 추적 정보, `-x`는 첫 오류 시 중단을 의미한다. **테스트 통과 여부는 사용자 환경에서 실행하여 확인해야 한다.**

## 11. 작업 순서 ⑨ 웹 서버 실행 및 기능 확인

```powershell
uv run python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/`에 접속한다. 상품 목록·검색·장바구니·주문·모의 결제·취소·환불·접근 권한 및 보고서 기능을 화면에서 확인한다. 실제 화면과 접근 경로는 `config/urls.py`의 URL 설정을 기준으로 확인한다.

상품이 0개로 표시되면 7절의 상품 등록 명령어와 `Product.objects.count()` 결과를 확인한다.

## 12. 오류별 점검표

| 오류 | 우선 점검 사항 |
|---|---|
| `(2002) Can't connect` | 컨테이너 실행 상태, 호스트·포트, 방화벽 |
| `(2005) Unknown server host '3308'` | `DB_HOST=127.0.0.1`, `DB_PORT=3308` 분리 |
| `(1045) Access denied` | 계정·비밀번호·접속 허용 호스트 및 기존 볼륨 |
| `(1146) shop_product doesn't exist` | `migrate`, 실제 DB 이름, 테이블 존재 여부 |
| pytest `SystemExit: 2` | 최초 DB 생성 오류, 테스트 DB 생성 권한 |
| 상품 목록 0개 | `seed_products.py` 실행 및 DB 데이터 개수 |
| `No such container` | `docker ps -a`에서 실제 컨테이너 이름 확인 |

## 13. 재실행 및 데이터 보호

일반적인 재실행에서는 `.env`를 다시 복사하거나 볼륨을 초기화할 필요가 없다.

```powershell
Set-Location C:\lab\chapter17_project
docker compose up -d
docker compose ps
uv run python manage.py check
uv run python -m scripts.verify_project
uv run python manage.py runserver
```

**금지:** 기존 데이터가 필요한 경우 `docker compose down -v`, `docker volume rm` 또는 데이터베이스 수동 삭제를 실행하지 않는다. `docker compose down`은 일반적으로 볼륨을 유지하지만 컨테이너는 중지·제거한다.

## 14. 최종 점검표

- [ ] Python 3.12.x / Django 5.2.7 버전 확인
- [ ] `.env`의 비밀번호·SECRET_KEY 및 포트 일치 확인
- [ ] MySQL 컨테이너 `healthy` 확인
- [ ] `manage.py check` 오류 없음
- [ ] 마이그레이션 적용 및 필수 테이블 존재
- [ ] 예제 상품 등록 및 목록 출력 확인
- [ ] `scripts.verify_project` 검증 성공
- [ ] 통합 테스트 및 전체 테스트 실행 결과 확인
- [ ] 브라우저에서 주요 기능 확인
- [ ] 실제 PG 결제 미사용 및 DB 볼륨 보존 확인

> 이 README는 첨부된 프로젝트의 `compose.yaml`, `.env.example`, `pyproject.toml`, `scripts` 파일에 맞춰 작성하였다. 실제 실행 환경의 테스트 성공 여부는 별도로 검증해야 한다.
