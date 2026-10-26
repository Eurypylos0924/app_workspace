"""답변형 게시판의 계층 관계·권한·정렬·삭제를 검증한다."""
import pytest
from django.urls import reverse
from boards.models import Board

pytestmark = pytest.mark.django_db

# 로그인한 회원이 게시글에 답글을 작성할 수 있는지 확인한다.
def test_create_reply(logged_in_client, board, member):
    response = logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "첫 답글", "content": "답변 내용"})
    assert response.status_code == 302
    reply = Board.objects.get(title="첫 답글")
    assert reply.parent_id == board.pk
    assert reply.author_id == member.pk
    assert reply.depth == 1
    assert reply.root_id == board.pk

# 답글의 답글을 작성하면 깊이와 원글 ID가 유지되는지 확인한다.
def test_nested_reply(logged_in_client, board):
    url = reverse("boards:reply", args=[board.pk])
    logged_in_client.post(url, {"title": "1단계", "content": "내용"})
    first = Board.objects.get(title="1단계")
    logged_in_client.post(reverse("boards:reply", args=[first.pk]), {"title": "2단계", "content": "내용"})
    second = Board.objects.get(title="2단계")
    assert second.depth == 2
    assert second.root_id == board.pk
    assert second.thread_path.startswith(first.thread_path + ".")

# 비로그인 사용자의 답글 작성은 로그인 화면으로 이동하는지 확인한다.
def test_reply_requires_login(client, board):
    response = client.post(reverse("boards:reply", args=[board.pk]), {"title": "차단", "content": "내용"})
    assert response.status_code == 302
    assert not Board.objects.filter(title="차단").exists()

# 게시판 목록에서 답글이 부모 글 다음에 나타나는지 확인한다.
def test_reply_list_order(logged_in_client, board):
    logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "순서 확인", "content": "내용"})
    response = logged_in_client.get(reverse("boards:list"))
    ids = [item.pk for item in response.context["page_obj"].object_list]
    reply = Board.objects.get(title="순서 확인")
    assert ids.index(reply.pk) == ids.index(board.pk) + 1

# 부모 게시글을 삭제하면 종속된 답글도 함께 삭제되는지 확인한다.
def test_delete_parent_cascades(logged_in_client, board):
    logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "삭제될 답글", "content": "내용"})
    reply = Board.objects.get(title="삭제될 답글")
    logged_in_client.post(reverse("boards:delete", args=[board.pk]))
    assert not Board.objects.filter(pk=reply.pk).exists()


# 원글을 생성하면 parent가 NULL이며 최상위 경로가 설정되는지 검증한다.
def test_original_post_has_no_parent(logged_in_client):
    response = logged_in_client.post(reverse("boards:create"), {"title": "원글", "content": "내용"})
    assert response.status_code == 302
    original = Board.objects.get(title="원글")
    assert original.parent_id is None
    assert original.root_id == original.pk
    assert original.depth == 0
    assert original.thread_path == f"{original.pk:012d}"

# 부모 게시글과 답글의 자기참조 역방향 관계가 작동하는지 검증한다.
def test_parent_replies_relation(logged_in_client, board):
    logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "관계 확인", "content": "내용"})
    reply = Board.objects.get(title="관계 확인")
    assert reply.parent == board
    assert board.replies.filter(pk=reply.pk).exists()

# 부모-자식-손자 답글을 순서대로 나열하는지 검증한다.
def test_nested_tree_order(logged_in_client, board):
    logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "첫 답글", "content": "내용"})
    first = Board.objects.get(title="첫 답글")
    logged_in_client.post(reverse("boards:reply", args=[first.pk]), {"title": "대댓글", "content": "내용"})
    nested = Board.objects.get(title="대댓글")
    logged_in_client.post(reverse("boards:reply", args=[board.pk]), {"title": "둘째 답글", "content": "내용"})
    second = Board.objects.get(title="둘째 답글")
    ids = list(Board.objects.order_by("-root_id", "thread_path", "id").values_list("pk", flat=True))
    assert ids.index(board.pk) < ids.index(first.pk) < ids.index(nested.pk) < ids.index(second.pk)
