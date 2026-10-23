"""제8장 Django 설정: SQLite가 아닌 MySQL을 사용한다."""
import os
from pathlib import Path
from dotenv import load_dotenv

# manage.py가 위치한 프로젝트 최상위 폴더이다.
BASE_DIR = Path(__file__).resolve().parent.parent
# 프로젝트 루트의 환경변수 파일을 불러온다.
load_dotenv(BASE_DIR / ".env")
# 예제 키를 실제 운영 키로 사용하지 못하도록 확인한다.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY == "replace-with-a-generated-secret":
    raise RuntimeError(".env의 DJANGO_SECRET_KEY를 안전한 값으로 설정해야 한다.")
# 실습에서만 True를 사용하며 운영 환경에서는 False로 설정한다.
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

   
    # shop 앱의 Product/Category 모델을 Django에 등록한다.
    "shop.apps.ShopConfig",
    "accounts.apps.AccountsConfig",
    # DRF의 APIView, Serializer, Browsable API를 사용한다.
    "rest_framework",
    # 상품 REST API를 제공하는 별도 앱이다.
    "api.apps.ApiConfig",
    # 주문 내역과 주문 상품을 저장하는 제13장 앱이다.
    "orders.apps.OrdersConfig",
    # 제16장 관리자 통계·CSV 앱을 등록한다.
    "reports.apps.ReportsConfig",
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
ASGI_APPLICATION = "config.asgi.application"
# DB 정보는 코드에 직접 기록하지 않고 .env에서 읽는다.
DATABASES = {"default": {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.getenv("MYSQL_DATABASE", "shopdb"),
    "USER": os.getenv("MYSQL_USER", "shopuser"),
    "PASSWORD": os.getenv("MYSQL_PASSWORD", ""),
    "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "PORT": os.getenv("MYSQL_PORT", "3308"),
    "OPTIONS": {"charset": "utf8mb4"},
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

# 로그인 이후 이동할 페이지와 로그인 화면의 URL 이름을 지정한다.
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "product_list"
LOGOUT_REDIRECT_URL = "product_list"
# 개발 중 정적 파일의 위치이다.
STATICFILES_DIRS = [BASE_DIR / "static"]

# DRF의 인증과 권한은 ViewSet에서 명시적으로 결정한다.
# 목록 API의 기본 페이지 크기는 10개이다.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
