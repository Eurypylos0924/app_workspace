"""회원과 게시글 테스트에서 공통으로 사용하는 pytest Fixture."""
import pytest
from boards.models import Board
from members.models import Member

# 테스트마다 독립된 회원을 생성하여 데이터 간섭을 방지한다.
@pytest.fixture
def member(db):
    return Member.objects.create_user(username="author_a", password="StrongPass!234", display_name="작성자", email="author_a@example.com")

# 다른 회원의 게시글 접근 권한을 검사하기 위한 계정을 생성한다.
@pytest.fixture
def other_member(db):
    return Member.objects.create_user(username="author_b", password="StrongPass!234", display_name="다른회원", email="author_b@example.com")

# 권한 검증에 사용할 기본 게시글을 생성한다.
@pytest.fixture
def board(member):
    board = Board.objects.create(author=member, title="원래 제목", content="원래 내용")
    Board.objects.filter(pk=board.pk).update(root_id=board.pk, thread_path=f"{board.pk:012d}")
    board.refresh_from_db()
    return board

# 인증이 필요한 테스트에서 사용할 로그인 클라이언트를 제공한다.
@pytest.fixture
def logged_in_client(client, member):
    client.force_login(member)
    return client

# 테스트에서 생성한 첨부파일이 실제 프로젝트 media 폴더를 오염시키지 않도록 격리한다.
@pytest.fixture(autouse=True)
def isolated_media(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"

