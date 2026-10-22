"""Django 홈 화면 HTTP 응답 확인."""

from django.test import Client


def test_home_page():
    # 테스트용 클라이언트로 홈 화면을 요청한다.
    response = Client().get("/")
    assert response.status_code == 200
    assert "Chapter 01 Django 개발환경" in response.content.decode("utf-8")
