"""회원가입, 로그인·로그아웃, 세션 및 회원 탈퇴를 검증한다."""
import pytest
from django.contrib.auth import SESSION_KEY
from django.urls import reverse
from boards.models import Board
from members.models import Member

pytestmark = pytest.mark.django_db

# 회원가입 POST 후 회원이 저장되고 로그인 세션이 생성되는지 확인한다.
def test_signup_creates_member_and_session(client):
    data = {"username": "tester01", "display_name": "테스터", "email": "tester01@example.com", "gender": "M", "age": 25, "phone": "010-1234-5678", "password1": "testpass1234!", "password2": "testpass1234!"}
    response = client.post(reverse("members:signup"), data)
    assert response.status_code == 302
    member = Member.objects.get(username="tester01")
    assert str(client.session[SESSION_KEY]) == str(member.pk)

# 실제 비밀번호 인증을 거친 로그인과 POST 로그아웃 후 세션 제거를 확인한다.
def test_login_logout_session(client, member):
    assert SESSION_KEY not in client.session
    response = client.post(reverse("members:login"), {"username": member.username, "password": "StrongPass!234"})
    assert response.status_code == 302
    assert str(client.session[SESSION_KEY]) == str(member.pk)
    assert client.get(reverse("members:profile")).status_code == 200
    assert client.post(reverse("members:logout")).status_code == 302
    assert SESSION_KEY not in client.session
    assert client.get(reverse("members:profile")).status_code == 302

# 회원 탈퇴는 POST에서만 수행하며 본인의 게시글만 CASCADE 삭제하는지 확인한다.
def test_withdraw_deletes_member_and_posts(logged_in_client, member, other_member, board):
    other_board = Board.objects.create(author=other_member, title="보존 글", content="보존")
    assert logged_in_client.get(reverse("members:withdraw")).status_code == 200
    assert Member.objects.filter(pk=member.pk).exists()
    assert logged_in_client.post(reverse("members:withdraw")).status_code == 302
    assert not Member.objects.filter(pk=member.pk).exists()
    assert not Board.objects.filter(pk=board.pk).exists()
    assert Board.objects.filter(pk=other_board.pk).exists()
    assert SESSION_KEY not in logged_in_client.session

# 잘못된 비밀번호로 로그인하면 인증 세션이 생성되지 않는지 확인한다.
def test_invalid_password_does_not_login(client, member):
    response = client.post(reverse("members:login"), {"username": member.username, "password": "wrong-password"})
    assert response.status_code == 200
    assert SESSION_KEY not in client.session

# 외부 사이트로의 next 리다이렉트가 차단되는지 확인한다.
def test_login_rejects_external_next(client, member):
    response = client.post(reverse("members:login") + "?next=https://attacker.example/", {"username": member.username, "password": "StrongPass!234"})
    assert response.status_code == 302
    assert response["Location"] == reverse("boards:list")
