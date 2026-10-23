"""회원 관리 앱의 Django 등록 설정이다."""
from django.apps import AppConfig
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
