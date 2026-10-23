from django.urls import path
from . import views

# URL 이름을 템플릿에서 역참조하여 경로 변경의 영향을 줄인다.
urlpatterns = [
    path("orders/<int:pk>/pay/", views.order_pay, name="order_pay"),
    path("orders/<int:pk>/refund/", views.order_refund, name="order_refund"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    # 취소와 확인은 모두 POST로만 호출한다.
    path("orders/<int:pk>/cancel/", views.order_cancel, name="order_cancel"),
    path("orders/<int:pk>/confirm/", views.order_confirm, name="order_confirm"),
]
