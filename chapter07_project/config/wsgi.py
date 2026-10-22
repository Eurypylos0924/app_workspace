# WSGI 서버가 Django를 실행할 때 쓰는 파일입니다.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
