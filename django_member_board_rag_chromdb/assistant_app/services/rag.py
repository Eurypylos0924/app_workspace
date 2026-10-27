
"""OpenAI text-embedding-3-small + ChromaDB 기반 RAG 검색."""

import os
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from django.conf import settings
from dotenv import load_dotenv
from pypdf import PdfReader


# --------------------------------------------------
# 1. 환경변수 및 임베딩 모델 설정
# --------------------------------------------------

# Django 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parents[2]

# 프로젝트 루트의 .env 파일 로드
load_dotenv(BASE_DIR / ".env")

# OpenAI 임베딩 모델
MODEL = "text-embedding-3-small"

# ChromaDB 컬렉션 이름에 모델 식별자를 포함한다.
COLLECTION_SUFFIX = "_openai3small"


# --------------------------------------------------
# 2. OpenAI 임베딩 함수
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_function():
    """OpenAI 임베딩 함수를 생성하고 재사용한다."""

    # 환경변수에 등록된 API 키를 확인한다.
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 설정되지 않았다. "
            "프로젝트 루트의 .env 파일을 확인해야 한다."
        )

    # API 키 자체가 아닌 환경변수 이름을 전달한다.
    return OpenAIEmbeddingFunction(
        api_key_env_var="OPENAI_API_KEY",
        model_name=MODEL,
    )


# --------------------------------------------------
# 3. ChromaDB 클라이언트
# --------------------------------------------------

@lru_cache(maxsize=1)
def client():
    """영속 저장 방식의 ChromaDB 클라이언트를 반환한다."""

    # ChromaDB 저장 디렉터리
    chroma_dir = Path(settings.CHROMA_DIR)

    # 디렉터리가 없으면 생성한다.
    chroma_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return chromadb.PersistentClient(
        path=str(chroma_dir)
    )


# --------------------------------------------------
# 4. ChromaDB 컬렉션
# --------------------------------------------------

def collection(name="policy_documents"):
    """임베딩 모델별 컬렉션을 생성하거나 가져온다."""

    collection_name = name + COLLECTION_SUFFIX

    return client().get_or_create_collection(
        name=collection_name,

        # 기존 코드의 _embedding() 오류 수정
        embedding_function=get_embedding_function(),

        # 코사인 거리 기반 검색
        metadata={
            "hnsw:space": "cosine",
        },
    )


# --------------------------------------------------
# 5. 문서 청크 분할
# --------------------------------------------------

def split_text(text, chunk_size=800, overlap=120):
    """문서를 일정한 크기의 중첩 청크로 분할한다."""

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size는 0보다 커야 한다."
        )

    if overlap < 0 or chunk_size <= overlap:
        raise ValueError(
            "overlap은 0 이상이며 chunk_size보다 작아야 한다."
        )

    # 연속된 공백과 줄바꿈을 정리한다.
    text = " ".join((text or "").split())

    if not text:
        return []

    # 청크 이동 간격
    step = chunk_size - overlap

    chunks = []

    for start in range(0, len(text), step):

        chunk = text[
            start:start + chunk_size
        ]

        if chunk.strip():
            chunks.append(chunk)

        # 마지막 청크까지 처리했으면 종료한다.
        if start + chunk_size >= len(text):
            break

    return chunks


# --------------------------------------------------
# 6. PDF 문서 색인
# --------------------------------------------------

def index_pdfs():
    """PDF 문서를 읽어 ChromaDB에 색인한다."""

    col = collection()

    docs = []
    ids = []
    metas = []

    # PDF 문서 디렉터리
    docs_dir = Path(settings.DATA_DIR) / "docs"

    if not docs_dir.exists():
        raise FileNotFoundError(
            f"PDF 문서 디렉터리가 없다: {docs_dir}"
        )

    pdf_files = sorted(
        docs_dir.glob("*.pdf")
    )

    # 기존 PDF 청크 목록을 조회한다.
    existing = col.get(
        include=["metadatas"]
    )

    # 현재 PDF 목록과 비교하여 삭제된 문서를 제거한다.
    current_sources = {
        pdf.name for pdf in pdf_files
    }

    stale_ids = [
        doc_id
        for doc_id, meta in zip(
            existing["ids"],
            existing["metadatas"] or []
        )
        if meta
        and meta.get("source") not in current_sources
    ]

    if stale_ids:
        col.delete(ids=stale_ids)

    for pdf in pdf_files:

        # 해당 PDF의 이전 청크를 삭제한다.
        col.delete(
            where={"source": pdf.name}
        )

        # PDF 페이지 읽기
        reader = PdfReader(str(pdf))

        for page_no, page in enumerate(
            reader.pages,
            start=1,
        ):

            page_text = page.extract_text() or ""

            chunks = split_text(page_text)

            for chunk_no, chunk in enumerate(chunks):

                # 고유 청크 ID
                doc_id = (
                    f"{pdf.name}:{page_no}:{chunk_no}"
                )

                ids.append(doc_id)

                docs.append(chunk)

                metas.append({
                    "source": pdf.name,
                    "page": page_no,
                    "chunk": chunk_no,
                })

    # ChromaDB에 50개씩 저장한다.
    batch_size = 50

    for start in range(0, len(ids), batch_size):

        end = start + batch_size

        col.upsert(
            ids=ids[start:end],
            documents=docs[start:end],
            metadatas=metas[start:end],
        )

    return len(ids)


# --------------------------------------------------
# 8. 공통 벡터 검색
# --------------------------------------------------

def _search(col, query, k):
    """ChromaDB에서 의미적으로 유사한 문서를 검색한다."""

    if not isinstance(query, str) or not query.strip():
        return []

    if k <= 0:
        return []

    total = col.count()

    if total == 0:
        return []

    result = col.query(
        query_texts=[query],
        n_results=min(k, total),
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = (result.get("documents") or [[]])[0]
    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]

    hits = []

    for text, meta, distance in zip(
        documents,
        metadatas,
        distances,
    ):

        distance = float(distance)

        # 코사인 거리를 유사도 형태로 변환한다.
        # 순위 비교를 위한 점수이며 확률은 아니다.
        score = max(
            0.0,
            min(1.0, 1.0 - distance),
        )

        hits.append({
            "text": text,
            **(meta or {}),
            "distance": round(distance, 4),
            "score": round(score, 4),
        })

    return hits


# --------------------------------------------------
# 9. PDF 문서 검색
# --------------------------------------------------

def search_documents(query, k=4):
    """PDF 정책 문서에서 관련 내용을 검색한다."""

    return _search(
        col=collection(),
        query=query,
        k=k,
    )




# 게시판 벡터 컬렉션: 원글과 답글을 각각 색인한다.
def board_collection():
    return collection("board_posts")


def index_board(board):
    """게시글 1건의 현재 제목·내용을 갱신한다."""
    col = board_collection()
    text = f"게시글 번호: {board.pk}\n제목: {board.title}\n내용: {board.content}"
    chunks = split_text(text, chunk_size=800, overlap=120)
    old = col.get(where={"board_id": board.pk})["ids"]
    if old:
        col.delete(ids=old)
    if chunks:
        col.upsert(
            ids=[f"board:{board.pk}:{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"kind":"board", "source":"게시판", "board_id":board.pk,
                        "title":board.title, "page":0, "url":f"/boards/{board.pk}/"}
                       for _ in chunks],
        )
    return len(chunks)


def delete_board(board_id):
    col = board_collection()
    ids = col.get(where={"board_id": int(board_id)})["ids"]
    if ids:
        col.delete(ids=ids)


def index_boards():
    from boards.models import Board
    col = board_collection()
    ids = col.get()["ids"]
    if ids:
        col.delete(ids=ids)
    total = 0
    for board in Board.objects.all().iterator():
        total += index_board(board)
    return total


_pdf_search = search_documents

def search_documents(query, k=4):
    """PDF 및 게시글 검색 결과를 유사도 기준으로 통합한다."""
    pdf_hits = _pdf_search(query, k=k)
    board_hits = _search(board_collection(), query, k=k)
    for hit in pdf_hits:
        hit.setdefault("kind", "pdf")
    return sorted(pdf_hits + board_hits, key=lambda x: x["score"], reverse=True)[:k]
