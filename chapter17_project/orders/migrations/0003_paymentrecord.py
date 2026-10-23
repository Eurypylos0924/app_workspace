# 제14장 주문 데이터를 보존하고 별도의 모의 결제 기록 테이블을 생성한다.
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [("orders", "0002_order_status_cancelled_at")]
    operations = [
        migrations.CreateModel(
            name="PaymentRecord",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("status", models.CharField(max_length=12, choices=[("paid", "모의 결제 완료"), ("refunded", "모의 환불 완료")], default="paid")),
                ("amount", models.DecimalField(max_digits=12, decimal_places=2)),
                ("paid_at", models.DateTimeField(auto_now_add=True)),
                ("refunded_at", models.DateTimeField(blank=True, null=True)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="payment", to="orders.order")),
            ],
        ),
    ]
