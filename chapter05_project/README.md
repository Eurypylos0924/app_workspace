# 제5장 Git·GitHub와 Django 상품 웹서비스

## 실습 환경
Windows PowerShell, Python 3.12(제1장 설치), uv, VS Code, Git.

## 실행
```powershell
uv sync
uv run python manage.py check
uv run python manage.py migrate
uv run pytest -v
uv run python manage.py runserver 8000
```

## Git·GitHub
```powershell
git init
git add .
git commit -m "feat: initialize Django shop"
git branch -M main
# GitHub에서 빈 저장소를 만든 뒤 실제 주소 사용
git remote add origin https://github.com/YOUR-ACCOUNT/chapter05-django-shop.git
git push -u origin main
```

`.env`, `.venv`, `db.sqlite3`는 Git에 포함하지 않는다.

## 접속 주소
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health/

## 참고
제5장은 SQLite로 Django의 기본 흐름을 확인하며, MySQL은 이후 장에서 연동한다.
