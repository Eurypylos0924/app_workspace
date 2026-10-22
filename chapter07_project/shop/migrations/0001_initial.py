# Product 모델을 MySQL 테이블로 만드는 마이그레이션입니다.
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("price", models.PositiveIntegerField()),
                ("stock", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["id"]},
        ),
    ]
