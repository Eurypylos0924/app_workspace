# 제1장 개발환경 실습 프로젝트 
 
Windows PowerShell에서 다음 순서대로 실행한다. 
 
```powershell 
uv python install 3.12 
uv sync 
Copy-Item .env.example .env 
$secret = uv run python -c "from django.core.management.utils import get_random_secret_key; 
print(get_random_secret_key())" 
(Get-Content .env) -replace '^DJANGO_SECRET_KEY=.*$', "DJANGO_SECRET_KEY=$secret" | Set-Content .env 
Encoding utf8 
uv run python hello.py 
uv run python check_environment.py 
uv run python manage.py check 
uv run python manage.py migrate 
uv run pytest -q 
uv run python manage.py runserver 127.0.0.1:8000 
``` 
 
브라우저: http://127.0.0.1:8000/  
 
`.env`는 비공개이며 `.env.example`만 공유한다. MySQL은 제7장에서 연결한다. 