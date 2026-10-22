# Django 프로젝트 설정입니다.
# .env 에 적은 MySQL 접속 정보를 읽어 Django ORM에 연결합니다.

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "insecure-local-chapter07-only")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 이번 장에서 만든 앱
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    # 프로젝트 공용 템플릿 폴더
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "config.wsgi.application"

# MySQL 접속 정보 (모두 .env 에서 읽어옵니다)
DATABASES = {"default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.environ.get("MYSQL_DATABASE", "shopdb"),
    "USER": os.environ.get("MYSQL_USER", "shopuser"),
    "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
    "HOST": os.environ.get("MYSQL_HOST", "127.0.0.1"),
    "PORT": os.environ.get("MYSQL_PORT", "3307"),
    "OPTIONS": {"charset": "utf8mb4"},
    # pytest가 사용할 별도의 테스트 DB 이름 (실제 데이터와 분리)
    "TEST": {"NAME": "test_" + os.environ.get("MYSQL_DATABASE", "shopdb")},
}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
