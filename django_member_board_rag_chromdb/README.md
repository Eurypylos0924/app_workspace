# Django Member Board MVT (MySQL 8.4 + uv + Python 3.12)

MySQL 8.4 Docker 컨테이너와 uv, Python 3.12 기반의 Django 회원/게시판 시스템입니다.

## 1. 주요 개발 환경
- **Package Manager**: `uv`
- **IDE**: VS Code (설정 파일 `.vscode/` 포함)
- **Python**: 3.12+
- **Database**: Docker MySQL 8.4 (포트 `3310`)

## 2. 데모 계정 정보
| 구분 | 아이디 | 비밀번호 | 권한 |
| :--- | :--- | :--- | :--- |
| 관리자 | `admin` | `admin1234!` | 최고 관리자 (`superuser`, `staff`) |
| 일반회원 1 | `user01` | `pass1234!` | 일반 회원 |
| 일반회원 2 | `user02` | `pass1234!` | 일반 회원 |

## 3. 실행 방법 (Windows / PowerShell 기준)

### 1) MySQL 8.4 Docker 컨테이너 실행
```bash
docker compose up -d
```
> `compose.yaml`을 통해 `shopdb`가 생성되며, Windows 호스트의 `3310` 포트로 연결됩니다.

### 2) uv 환경 구축 및 의존성 동기화
```bash
uv venv --python 3.12
uv add mysqlclient
uv sync
```

### 3) 데이터베이스 마이그레이션 적용
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 4) 데모 계정 및 초기 데이터 시드
```bash
uv run python manage.py seed_demo
```

### 5) Django 개발 서버 실행
```bash
uv run python manage.py runserver
```

웹 브라우저에서 `http://127.0.0.1:8000/` 으로 접속합니다.
