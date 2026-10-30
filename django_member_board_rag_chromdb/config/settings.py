"""Django 프로젝트의 전역 환경설정 파일입니다."""
# 파일 시스템 경로 계산을 위해 Path 클래스를 가져옵니다.
from pathlib import Path
# 환경변수 값을 읽기 위해 os 모듈을 가져옵니다.
import os
# 프로젝트 루트의 .env 파일을 읽기 위해 python-dotenv 함수를 가져옵니다.
from dotenv import load_dotenv


# manage.py가 위치한 프로젝트 최상위 폴더이다.
BASE_DIR = Path(__file__).resolve().parent.parent
# 프로젝트 루트의 환경변수 파일을 불러온다.
load_dotenv(BASE_DIR / ".env")

# 세션, CSRF 토큰, 비밀번호 재설정 등에 사용하는 비밀키를 환경변수에서 읽습니다.
# 예제 키를 실제 운영 키로 사용하지 못하도록 확인한다.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY == "replace-with-a-generated-secret":
    raise RuntimeError(".env의 DJANGO_SECRET_KEY를 안전한 값으로 설정해야 한다.")
# 실습에서만 True를 사용하며 운영 환경에서는 False로 설정한다.
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# 쉼표로 구분된 호스트 문자열을 리스트로 변환합니다.
ALLOWED_HOSTS = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",") if host.strip()]

# Django 기본 앱과 프로젝트에서 만든 앱을 등록합니다.
INSTALLED_APPS = [
    # Django 관리자 사이트 기능을 제공합니다.
    "django.contrib.admin",
    # 로그인, 로그아웃, 사용자/권한 모델 기능을 제공합니다.
    "django.contrib.auth",
    # 모델 ContentType 정보를 관리합니다.
    "django.contrib.contenttypes",
    # 세션 데이터를 DB에 저장하고 로그인 상태를 유지합니다.
    "django.contrib.sessions",
    # 일회성 성공/오류 메시지를 화면에 출력하도록 지원합니다.
    "django.contrib.messages",
    # CSS, JavaScript, 이미지 등의 정적 파일을 관리합니다.
    "django.contrib.staticfiles",

    # 사용자 정의 회원 모델과 회원 기능을 제공하는 앱입니다.
     # DRF의 APIView, Serializer, Browsable API를 사용한다.
    "rest_framework",

    # # 사용자 정의 회원 모델(Member) 및 인증(회원가입/로그인/프로필) 기능을 제공하는 앱입니다.
    "members",
    # 게시글 CRUD 및 파일 첨부 기능을 제공하는 게시판 앱입니다.
    "boards",
    
    # rag
    "assistant_app",
]

# HTTP 요청/응답 과정에 적용할 미들웨어를 순서대로 등록합니다.
MIDDLEWARE = [
    # 보안 관련 기본 헤더와 설정을 적용합니다.
    "django.middleware.security.SecurityMiddleware",
    # 세션 객체 request.session을 사용할 수 있게 합니다.
    "django.contrib.sessions.middleware.SessionMiddleware",
    # URL 처리 전 공통적인 요청 정규화를 수행합니다.
    "django.middleware.common.CommonMiddleware",
    # POST 요청 위조를 방지하기 위해 CSRF 검증을 수행합니다.
    "django.middleware.csrf.CsrfViewMiddleware",
    # 세션의 사용자 ID를 바탕으로 request.user를 구성합니다.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # messages.success(), messages.error() 같은 메시지 기능을 제공합니다.
    "django.contrib.messages.middleware.MessageMiddleware",
    # 클릭재킹 공격을 완화하기 위한 X-Frame-Options 헤더를 적용합니다.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 프로젝트의 최상위 URL 설정 모듈을 지정합니다.
ROOT_URLCONF = "config.urls"

# Django 템플릿 엔진과 공통 템플릿 경로를 설정합니다.
TEMPLATES = [
    {
        # Django 기본 템플릿 백엔드를 사용합니다.
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 프로젝트 루트/templates 폴더에서도 템플릿을 찾도록 합니다.
        "DIRS": [BASE_DIR / "templates"],
        # 각 앱 내부의 templates 폴더를 자동 검색합니다.
        "APP_DIRS": True,
        # 템플릿에서 debug, request, user, messages 등을 사용하기 위한 Context Processor를 설정합니다.
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI 웹 서버가 사용할 애플리케이션 객체 위치를 지정합니다.
WSGI_APPLICATION = "config.wsgi.application"
# ASGI 웹 서버가 사용할 애플리케이션 객체 위치를 지정합니다.
ASGI_APPLICATION = "config.asgi.application"

# MySQL 데이터베이스 연결 정보를 환경변수 기반으로 설정합니다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE") or os.getenv("DB_NAME", "shopdb"),
        "USER": os.getenv("MYSQL_USER") or os.getenv("DB_USER", "shopuser"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD") or os.getenv("DB_PASSWORD", "changeapp1234"),
        "HOST": os.getenv("MYSQL_HOST") or os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT") or os.getenv("DB_PORT", "3310"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
        
    }
}

# Django 내장 비밀번호 유효성 검사 규칙 목록 설정
# 사용자가 회원가입이나 비밀번호 변경 시 안전하지 않은 비밀번호를 입력하지 못하도록 차단합니다.
AUTH_PASSWORD_VALIDATORS = [
    # 1. 사용자 정보 유사도 검사기
    # 아이디, 이름, 이메일 등 사용자 프로필 정보와 지나치게 유사한 비밀번호 입력을 방지합니다.
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    # 2. 최소 길이 검사기
    # 비밀번호의 최소 글자 수를 제한합니다 (기본값: 최소 8자 이상).
    # 필요한 경우 OPTIONS를 통해 {'min_length': 10} 등으로 최소 길이를 조정할 수 있습니다.
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # 3. 통상적인 비밀번호 검사기
    # 'password', '12345678', 'qwerty' 등 전 세계적으로 흔히 쓰이는 20,000여 개의 쉬운 비밀번호 사전과 비교하여 차단합니다.
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    # 4. 순수 숫자 비밀번호 검사기
    # 비밀번호 전체가 숫자로만 구성된 경우(예: '12341234') 입력을 제한하고 영문이나 특수문자 조합을 유도합니다.
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 프로젝트에서 기본 auth.User 대신 members.Member 모델을 사용자 모델로 사용합니다.
AUTH_USER_MODEL = "members.Member"
# @login_required에서 로그인하지 않은 사용자를 이동시킬 URL 이름입니다.
LOGIN_URL = "members:login"
# 로그인 성공 후 next 값이 없을 때 이동할 기본 URL입니다.
LOGIN_REDIRECT_URL = "boards:list"
# 로그아웃 후 이동할 기본 URL입니다.
LOGOUT_REDIRECT_URL = "home"
# 사용자의 비활성 시간이 30분을 넘으면 세션을 만료시킵니다.
SESSION_COOKIE_AGE = 30 * 60
# 요청이 발생할 때마다 세션 만료 시간을 다시 30분으로 연장합니다.
SESSION_SAVE_EVERY_REQUEST = True

# 사이트의 기본 언어를 한국어로 지정합니다.
LANGUAGE_CODE = "ko-kr"
# 서버와 템플릿에서 사용하는 표준 시간대를 서울로 지정합니다.
TIME_ZONE = "Asia/Seoul"
# Django 번역 기능을 활성화합니다.
USE_I18N = True
# timezone-aware datetime을 사용합니다.
USE_TZ = True

# /static/ URL이 정적 파일을 가리키도록 설정합니다.
STATIC_URL = "/static/"
# 프로젝트 공통 static 디렉터리를 추가합니다.
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# 업로드한 프로필 사진과 게시글 첨부파일의 URL 접두사를 지정합니다.
MEDIA_URL = "/media/"
# 업로드 파일을 실제 저장할 디렉터리를 지정합니다.
MEDIA_ROOT = BASE_DIR / "media"
# AutoField보다 큰 정수형 기본 PK 타입을 사용합니다.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# PDF 및 게시글 벡터 색인 저장 경로
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_store"

# AWS HTTPS reverse proxy settings
CSRF_TRUSTED_ORIGINS = [v.strip() for v in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if v.strip()]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "False").lower() == "true"
SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", "False").lower() == "true"
CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", "False").lower() == "true"


import os

# 개발환경과 운영환경 구분
DEBUG = os.getenv(
    "DJANGO_DEBUG", "False"
).lower() == "true"

# 운영환경에서만 보안 설정 적용
if not DEBUG:
    # 	HTTP 요청을 HTTPS로 전환
    SECURE_SSL_REDIRECT = (
        os.getenv("DJANGO_SECURE_SSL_REDIRECT", "False")
        .lower() == "true"
    )

    # 세션 쿠키를 HTTPS로만 전
    SESSION_COOKIE_SECURE = (
        os.getenv("DJANGO_SESSION_COOKIE_SECURE", "False")
        .lower() == "true"
    )

   # CSRF 쿠키를 HTTPS로만 전송
    CSRF_COOKIE_SECURE = (
        os.getenv("DJANGO_CSRF_COOKIE_SECURE", "False")
        .lower() == "true"
    )

    # 프록시가 전달한 HTTPS 정보 인식
    # 신뢰할 수 있는 프록시에서 HTTPS를 종료할 때만 사용한다.
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    # 브라우저에 HTTPS 사용 정책 전달
    SECURE_HSTS_SECONDS = int(
        os.getenv("DJANGO_SECURE_HSTS_SECONDS", "0")
    )

    
