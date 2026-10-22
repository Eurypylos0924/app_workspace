# ASGI 서버가 Django를 실행할 때 쓰는 파일입니다.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_asgi_application()
