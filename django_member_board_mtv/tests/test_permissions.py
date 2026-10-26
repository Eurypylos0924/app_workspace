"""비로그인 접근 차단, 타인 게시글 권한, 관리자 권한을 검증한다."""
from urllib.parse import urlparse
import pytest
from django.urls import reverse
from boards.models import Board

pytestmark = pytest.mark.django_db

# 비로그인 사용자의 게시글 등록·수정·삭제 POST가 로그인 화면으로 이동하는지 확인한다.
@pytest.mark.parametrize("action", ["create", "update", "delete"])
def test_anonymous_cannot_write(client, board, action):
    url = reverse("boards:create") if action == "create" else reverse(f"boards:{action}", args=[board.pk])
    response = client.post(url, {"title": "침입 제목", "content": "침입 내용"})
    assert response.status_code == 302
    assert urlparse(response["Location"]).path == reverse("members:login")
    board.refresh_from_db()
    assert board.title == "원래 제목"
    assert Board.objects.count() == 1

# 다른 일반 회원의 수정·삭제 GET/POST 요청이 403으로 거절되는지 확인한다.
@pytest.mark.parametrize("action", ["update", "delete"])
def test_other_member_forbidden(client, other_member, board, action):
    client.force_login(other_member)
    url = reverse(f"boards:{action}", args=[board.pk])
    assert client.get(url).status_code == 403
    assert client.post(url, {"title": "무단 수정", "content": "내용"}).status_code == 403
    board.refresh_from_db()
    assert board.title == "원래 제목"
    assert Board.objects.filter(pk=board.pk).exists()

# 관리자에게 타인 게시글 삭제는 허용하지만 수정은 금지하는 정책을 검증한다.
def test_staff_can_delete_but_not_edit(client, other_member, board):
    other_member.is_staff = True
    other_member.save(update_fields=["is_staff"])
    client.force_login(other_member)
    assert client.post(reverse("boards:update", args=[board.pk]), {"title": "관리자 수정", "content": "내용"}).status_code == 403
    assert client.post(reverse("boards:delete", args=[board.pk])).status_code == 302
    assert not Board.objects.filter(pk=board.pk).exists()
