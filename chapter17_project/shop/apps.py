"""shop 앱의 등록 정보를 정의한다."""
from django.apps import AppConfig

class ShopConfig(AppConfig):
    # 기본 PK를 64비트 정수 자동 증가로 생성한다.
    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"
