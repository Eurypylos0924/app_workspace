FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends build-essential pkg-config default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project && uv pip install --python .venv/bin/python 'gunicorn>=23,<24'
COPY . .
# 이미지 빌드 단계에서만 사용하는 임시 Django SECRET_KEY
RUN DJANGO_SECRET_KEY=build-only-not-for-production-0123456789 \
    .venv/bin/python manage.py collectstatic --noinput
EXPOSE 8000
CMD [".venv/bin/gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
