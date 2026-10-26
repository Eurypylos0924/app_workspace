"""게시글 목록/상세/등록/수정/삭제 CRUD와 소유권 검사를 담당합니다."""
# 로그인 제한 View에 사용할 데코레이터를 가져옵니다.
from django.contrib.auth.decorators import login_required
# 성공/오류 메시지를 화면에 전달하기 위한 messages를 가져옵니다.
from django.contrib import messages
# 페이지 단위로 게시글을 나누기 위한 Paginator를 가져옵니다.
from django.core.paginator import Paginator
# 권한이 없을 때 HTTP 403을 발생시킬 예외를 가져옵니다.
from django.core.exceptions import PermissionDenied
# 조회수를 안전하게 DB에서 1 증가시키기 위한 F 표현식을 가져옵니다.
from django.db.models import F, Q
from django.db import transaction
# 렌더링, 객체 조회, 리다이렉트 단축 함수를 가져옵니다.
from django.shortcuts import get_object_or_404, redirect, render
# 게시글 입력 폼을 가져옵니다.
from .forms import BoardForm
# 게시글 모델을 가져옵니다.
from .models import Board


def board_list(request):
    query = request.GET.get("q", "").strip()
    # 원글은 최신순, 각 원글의 답글은 부모-자식 경로순으로 정렬한다.
    board_queryset = Board.objects.select_related("author", "parent").all().order_by("-root_id", "thread_path", "id")

    if query:
        # 제목이나 본문에 검색어가 있는 게시글을 찾는다.
        board_queryset = board_queryset.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # 1페이지당 게시글 수: 10개
    paginator = Paginator(board_queryset, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # --- 10페이지 단위 블록 계산 ---
    page = page_obj.number               # 현재 페이지
    page_block = 10                      # 블록당 표시할 페이지 개수

    # 현재 블록의 시작 페이지 (1, 11, 21, ...)
    start_page = ((page - 1) // page_block) * page_block + 1
    # 현재 블록의 끝 페이지 (10, 20, 30, ...)
    end_page = start_page + page_block - 1

    # 전체 페이지 수가 블록 끝 번호보다 작으면 전체 페이지 수로 제한
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    custom_page_range = range(start_page, end_page + 1)

    # 이전 블록(11페이지 이상부터 활성화)
    has_prev_block = start_page > 1
    prev_block_page = start_page - 1

    # 다음 블록: 전체 페이지 수가 10페이지를 초과하고, 현재 블록 끝 페이지 뒤에 페이지가 더 있을 때만 활성화
    has_next_block = (paginator.num_pages > 10) and (end_page < paginator.num_pages)
    next_block_page = end_page + 1

    context = {
        "page_obj": page_obj,
        "query": query,
        "custom_page_range": custom_page_range,
        "has_prev_block": has_prev_block,
        "has_next_block": has_next_block,
        "prev_block_page": prev_block_page,
        "next_block_page": next_block_page,
    }
    return render(request, "boards/board_list.html", context)


def board_detail(request, pk):
    """게시글 상세 내용을 출력하고 조회수를 1 증가시킵니다."""
    # 작성자 정보와 함께 PK에 해당하는 게시글을 조회합니다.
    board = get_object_or_404(Board.objects.select_related("author"), pk=pk)
    # F 표현식을 사용하면 동시 요청에서도 현재 DB 값 기준으로 +1 UPDATE가 수행됩니다.
    Board.objects.filter(pk=board.pk).update(read_count=F("read_count") + 1)
    # 화면에 최신 조회수를 표시하기 위해 현재 객체 값을 1 증가시킵니다.
    board.read_count += 1
    # 상세 페이지를 출력합니다.
    return render(request, "boards/board_detail.html", {"board": board})


@login_required
def board_create(request):
    """로그인한 회원만 새 게시글을 등록할 수 있습니다."""
    # POST이면 전송 데이터와 파일을 폼에 바인딩하고 GET이면 빈 폼을 만듭니다.
    form = BoardForm(request.POST or None, request.FILES or None)
    # POST이면서 폼 검증에 성공한 경우 DB에 INSERT합니다.
    if request.method == "POST" and form.is_valid():
        # 작성자 값을 request.user로 넣기 위해 commit=False로 아직 DB 저장하지 않습니다.
        board = form.save(commit=False)
        # 작성자 조작을 막기 위해 브라우저 입력값이 아니라 로그인 세션의 사용자를 지정합니다.
        board.author = request.user
        # 최종 게시글을 ORM save()로 DB에 INSERT합니다.
        board.save()
        # 원글의 ID를 트리 그룹 ID로 사용한다.
        board.root_id = board.pk
        board.thread_path = f"{board.pk:012d}"
        board.save(update_fields=["root_id", "thread_path"])
        messages.success(request, "게시글이 등록되었습니다.")
        # 작성한 글 상세 화면으로 이동합니다.
        return redirect("boards:list")
    # 등록 폼을 출력합니다.
    return render(request, "boards/board_form.html", {"form": form, "mode": "등록"})


@login_required
def board_reply(request, pk):
    """로그인한 회원이 지정된 게시글에 답글을 등록한다."""
    parent = get_object_or_404(Board, pk=pk)
    form = BoardForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            # 부모 글을 잠가 동시 답글 작성 시 순서 충돌을 방지한다.
            parent = Board.objects.select_for_update().get(pk=pk)
            # 깊이 제한은 지나치게 긴 경로와 과도한 들여쓰기를 방지한다.
            if parent.depth >= 20:
                form.add_error(None, "답글은 최대 20단계까지 작성할 수 있습니다.")
            else:
                board = form.save(commit=False)
                board.author = request.user
                board.parent = parent
                board.root_id = parent.root_id or parent.pk
                board.depth = parent.depth + 1
                # 답글 경로는 부모 경로와 신규 PK의 12자리 문자열로 구성한다.
                prefix = parent.thread_path or f"{parent.pk:012d}"
                if len(prefix) + 13 > Board._meta.get_field("thread_path").max_length:
                    form.add_error(None, "답글 정렬 경로가 허용 길이를 초과했습니다.")
                else:
                    board.save()
                    board.thread_path = f"{prefix}.{board.pk:012d}"
                    board.save(update_fields=["thread_path"])
                    messages.success(request, "답글이 등록되었습니다.")
                    return redirect("boards:detail", pk=board.pk)
    return render(request, "boards/board_form.html", {
        "form": form, "mode": "답글 등록", "parent_board": parent,
    })


@login_required
def board_update(request, pk):
    """작성자 본인만 게시글을 수정할 수 있습니다."""
    # URL PK로 수정 대상 게시글을 조회합니다.
    board = get_object_or_404(Board, pk=pk)
    # 모델의 can_edit()로 본인 글인지 검사합니다.
    if not board.can_edit(request.user):
        # 관리자를 포함해 작성자가 아니면 수정은 허용하지 않고 403을 반환합니다.
        raise PermissionDenied("본인이 작성한 게시글만 수정할 수 있습니다.")
    # 기존 게시글 인스턴스에 입력값을 바인딩하여 UPDATE 폼을 만듭니다.
    form = BoardForm(request.POST or None, request.FILES or None, instance=board)
    # POST 요청이며 유효성 검사에 성공하면 UPDATE합니다.
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "게시글이 수정되었습니다.")
        return redirect("boards:detail", pk=board.pk)
    # 수정 폼을 출력합니다.
    return render(request, "boards/board_form.html", {"form": form, "mode": "수정", "board": board})


@login_required
def board_delete(request, pk):
    """작성자 본인 또는 관리자만 게시글을 삭제할 수 있습니다."""
    # 삭제 대상 게시글을 작성자 정보와 함께 조회합니다.
    board = get_object_or_404(Board.objects.select_related("author"), pk=pk)
    # 작성자 또는 관리자 여부를 검사합니다.
    if not board.can_delete(request.user):
        # 권한이 없으면 403 Forbidden을 발생시킵니다.
        raise PermissionDenied("본인 글만 삭제할 수 있습니다.")
    # GET 요청에서는 바로 지우지 않고 삭제 확인 화면을 보여줍니다.
    if request.method == "POST":
        # 하위 답글까지 수집하여 연쇄 삭제 시 파일도 정리한다.
        descendants = [board]
        queue = [board.pk]
        while queue:
            children = list(Board.objects.filter(parent_id__in=queue))
            descendants.extend(children)
            queue = [child.pk for child in children]
        attachments = [(item.attachment.storage, item.attachment.name)
                       for item in descendants if item.attachment and item.attachment.name]
        with transaction.atomic():
            board.delete()
            # DB 삭제가 커밋된 후에만 파일을 삭제한다.
            def remove_files():
                for storage, name in attachments:
                    storage.delete(name)
            transaction.on_commit(remove_files)
        messages.success(request, "게시글이 삭제되었습니다.")
        return redirect("boards:list")
    # 삭제 확인 화면을 출력합니다.
    return render(request, "boards/board_confirm_delete.html", {"board": board})
