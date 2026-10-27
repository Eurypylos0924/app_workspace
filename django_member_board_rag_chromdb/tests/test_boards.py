"""게시판 CRUD, 검색, 페이지네이션, 조회수, 첨부파일을 검증한다."""
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from boards.models import Board

pytestmark = pytest.mark.django_db

# 비로그인 사용자도 게시글 목록을 조회할 수 있는지 확인한다.
def test_board_list_page(client):
    response = client.get(reverse("boards:list"))
    assert response.status_code == 200
    assert "게시판" in response.content.decode("utf-8")

# 작성자가 게시글을 등록·수정·삭제하면 DB에 정확히 반영되는지 확인한다.
def test_board_crud(logged_in_client, member):
    response = logged_in_client.post(reverse("boards:create"), {"title": "테스트 게시글 제목", "content": "본문 내용"})
    assert response.status_code == 302
    board = Board.objects.get(title="테스트 게시글 제목")
    assert board.author_id == member.pk
    assert logged_in_client.get(reverse("boards:detail", args=[board.pk])).status_code == 200
    assert logged_in_client.post(reverse("boards:update", args=[board.pk]), {"title": "수정 제목", "content": "수정 내용"}).status_code == 302
    board.refresh_from_db()
    assert board.title == "수정 제목"
    assert logged_in_client.post(reverse("boards:delete", args=[board.pk])).status_code == 302
    assert not Board.objects.filter(pk=board.pk).exists()

# 제목에 검색어가 포함된 게시글만 반환하는지 확인한다.
def test_search_title_and_content(client, member):
    Board.objects.create(author=member, title="파이썬 검색", content="내용")
    Board.objects.create(author=member, title="다른 제목", content="파이썬 본문")
    response = client.get(reverse("boards:list"), {"q": "파이썬"})
    assert response.status_code == 200
    results = list(response.context["page_obj"].object_list)
    assert len(results) == 2
    assert {item.title for item in results} == {"파이썬 검색", "다른 제목"}

# 23개 게시글을 페이지당 10개씩 분할하고 잘못된 페이지 값을 처리하는지 확인한다.
def test_pagination(client, member):
    Board.objects.bulk_create([Board(author=member, title=f"글 {i}", content="내용") for i in range(23)])
    url = reverse("boards:list")
    responses = [client.get(url, {"page": number}) for number in (1, 2, 3)]
    assert [len(response.context["page_obj"].object_list) for response in responses] == [10, 10, 3]
    assert responses[2].context["page_obj"].paginator.num_pages == 3
    assert client.get(url, {"page": "invalid"}).context["page_obj"].number == 1

# 상세 페이지를 한 번 열면 조회수가 1 증가하는지 확인한다.
def test_detail_increases_read_count(client, board):
    before = board.read_count
    assert client.get(reverse("boards:detail", args=[board.pk])).status_code == 200
    board.refresh_from_db()
    assert board.read_count == before + 1

# 업로드한 파일이 저장되고 게시글 삭제 시 실제 파일도 제거되는지 확인한다.
@pytest.mark.django_db(transaction=True)
def test_attachment_upload_and_delete(logged_in_client, tmp_path):
    with override_settings(MEDIA_ROOT=tmp_path):
        upload = SimpleUploadedFile("sample.txt", b"attachment test", content_type="text/plain")
        response = logged_in_client.post(reverse("boards:create"), {"title": "파일 글", "content": "내용", "attachment": upload})
        assert response.status_code == 302
        board = Board.objects.get(title="파일 글")
        path = tmp_path / board.attachment.name
        assert path.exists()
        assert path.read_bytes() == b"attachment test"
        assert logged_in_client.post(reverse("boards:delete", args=[board.pk])).status_code == 302
        assert not Board.objects.filter(pk=board.pk).exists()
        assert not path.exists()
