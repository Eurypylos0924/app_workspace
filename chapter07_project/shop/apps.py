# Django에 shop 앱을 등록하는 설정입니다.
from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"
