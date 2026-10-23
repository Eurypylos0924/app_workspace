# Generated for the chapter 8 teaching example; Django 5.2-compatible initial migration.
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    # 이 앱의 첫 번째 마이그레이션이다.
    initial = True
    dependencies = []
    operations = [
        # shop_category 테이블을 생성한다.
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="분류명")),
            ],
            options={"verbose_name": "상품 분류", "verbose_name_plural": "상품 분류", "ordering": ["name"]},
        ),
        # shop_product 테이블과 category_id 외래키를 생성한다.
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="상품명")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="가격")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="재고")),
                ("description", models.TextField(blank=True, verbose_name="설명")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="등록일")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="shop.category", verbose_name="상품 분류")),
            ],
            options={"verbose_name": "상품", "verbose_name_plural": "상품", "ordering": ["id"]},
        ),
    ]
