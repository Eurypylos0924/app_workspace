# Django 앱 설정을 정의한다.
from django.apps import AppConfig

class ReportsConfig(AppConfig):
    # 자동 기본 키 타입을 Django 권장값으로 지정한다.
    default_auto_field = "django.db.models.BigAutoField"
    # INSTALLED_APPS에 등록할 앱 이름이다.
    name = "reports"
