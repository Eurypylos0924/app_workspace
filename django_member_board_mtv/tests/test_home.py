"""홈 화면의 렌더링과 최근 게시글 노출을 검증한다."""
import pytest
from django.urls import reverse
from boards.models import Board

pytestmark = pytest.mark.django_db

# 비로그인 사용자도 홈 화면에 정상 접근할 수 있는지 확인한다.
def test_home_page(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "Django Shop MTV" in response.content.decode("utf-8")

# 홈 화면에서 최근 게시글 최대 5개를 전달하는지 확인한다.
def test_home_recent_posts(client, member):
    Board.objects.bulk_create([Board(author=member, title=f"최근 글 {i}", content="내용") for i in range(7)])
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert len(response.context["recent_posts"]) == 5
