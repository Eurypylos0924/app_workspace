# HTTP 요청으로 화면이 잘 나오는지 확인하는 뷰 테스트입니다.
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_list_page(client):
    # 상품이 없어도 목록 화면은 HTTP 200 이어야 합니다.
    response = client.get(reverse("shop:product_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_missing_product_returns_404(client):
    # 없는 상품을 요청하면 HTTP 404 가 나와야 합니다.
    response = client.get(
        reverse("shop:product_detail", kwargs={"pk": 999999})
    )
    assert response.status_code == 404
