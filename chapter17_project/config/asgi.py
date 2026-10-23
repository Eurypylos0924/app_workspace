"""Django ASGI 서버의 진입점이다."""
import os
from django.core.asgi import get_asgi_application
# 웹 서버가 Django 설정을 찾도록 설정한다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# 서버가 호출하는 Django 애플리케이션 객체이다.
application = get_asgi_application()
