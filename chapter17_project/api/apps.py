"""REST API 앱을 Django에 등록한다."""
from django.apps import AppConfig

class ApiConfig(AppConfig):
    # 기존 shop 앱의 데이터베이스 테이블을 그대로 사용한다.
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
