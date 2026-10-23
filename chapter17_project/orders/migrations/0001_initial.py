# Django 5.2.7에서 Order 및 OrderItem 모델에 대해 생성하는 초기 마이그레이션이다.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("shop", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Order", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("total_amount", models.DecimalField(decimal_places=2, max_digits=12)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-created_at", "-id"]}),
        migrations.CreateModel(name="OrderItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("product_name", models.CharField(max_length=120)),
            ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ("quantity", models.PositiveIntegerField()),
            ("subtotal", models.DecimalField(decimal_places=2, max_digits=12)),
            ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="shop.product")),
        ]),
        migrations.AddConstraint(model_name="orderitem", constraint=models.UniqueConstraint(fields=("order", "product"), name="unique_order_product")),
    ]
