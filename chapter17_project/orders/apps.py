from django.apps import AppConfig

class OrdersConfig(AppConfig):
    # Django가 주문 앱의 모델과 설정을 찾을 수 있도록 앱을 등록한다.
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
