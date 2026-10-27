"""회원가입부터 게시글 CRUD 및 로그아웃까지 실제 HTTP 흐름을 검증한다."""
import pytest
from django.contrib.auth import SESSION_KEY
from django.urls import reverse
from boards.models import Board
from members.models import Member

pytestmark = pytest.mark.django_db

# 회원가입 → 로그아웃 → 실제 로그인 → 게시글 등록·수정·삭제 → 로그아웃 흐름을 확인한다.
def test_member_board_full_flow(client):
    signup = {"username": "flow_user", "display_name": "통합테스트", "email": "flow@example.com", "gender": "M", "age": 25, "phone": "010-1234-5678", "password1": "testpass1234!", "password2": "testpass1234!"}
    assert client.post(reverse("members:signup"), signup).status_code == 302
    member = Member.objects.get(username="flow_user")
    assert str(client.session[SESSION_KEY]) == str(member.pk)
    assert client.post(reverse("members:logout")).status_code == 302
    assert SESSION_KEY not in client.session
    assert client.post(reverse("members:login"), {"username": member.username, "password": "testpass1234!"}).status_code == 302
    assert str(client.session[SESSION_KEY]) == str(member.pk)
    assert client.post(reverse("boards:create"), {"title": "통합 글", "content": "등록 내용"}).status_code == 302
    board = Board.objects.get(title="통합 글", author=member)
    assert client.get(reverse("boards:detail", args=[board.pk])).status_code == 200
    assert client.post(reverse("boards:update", args=[board.pk]), {"title": "통합 수정", "content": "수정 내용"}).status_code == 302
    board.refresh_from_db()
    assert board.title == "통합 수정"
    assert client.post(reverse("boards:delete", args=[board.pk])).status_code == 302
    assert not Board.objects.filter(pk=board.pk).exists()
    assert client.post(reverse("members:logout")).status_code == 302
    assert SESSION_KEY not in client.session
