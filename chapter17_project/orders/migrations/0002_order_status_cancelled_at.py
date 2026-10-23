# 제13장의 기존 주문 데이터를 유지하면서 상태 필드와 취소 시각을 추가한다.
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("orders", "0001_initial")]
    operations = [
        migrations.AddField(
            model_name="order", name="status",
            field=models.CharField(max_length=12, choices=[("pending", "접수"), ("confirmed", "확인"), ("cancelled", "취소")], default="pending"),
        ),
        migrations.AddField(
            model_name="order", name="cancelled_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
