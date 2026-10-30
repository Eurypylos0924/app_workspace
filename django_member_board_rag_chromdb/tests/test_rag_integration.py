from unittest.mock import patch
from assistant_app.services.agent import answer
from assistant_app.services.rag import split_text

def test_chunking():
    assert split_text("hello world", 8, 2)

def test_merged_rag_fallback():
    hits = [{"kind":"board", "source":"게시판", "board_id":1,
             "title":"반품 문의", "page":0, "text":"반품 신청 방법", "score":0.9}]
    with patch("assistant_app.services.agent.search_documents", return_value=hits):
        with patch("assistant_app.services.agent.generate_answer", side_effect=RuntimeError("offline")):
            result = answer("반품 문의")
            
    # RAG 에이전트가 선택되었는지 확인한다.
    assert result["agent"] == "rag"

    # LLM 장애 상황에서도 검색 자료가 반환되는지 확인한다.
    assert "검색된 자료를 바탕으로 안내한다" in result["answer"]

    # 게시판 검색 결과가 포함되는지 확인한다.
    assert "반품 문의" in result["answer"]

    # 검색된 자료의 내용이 포함되는지 확인한다.
    assert "반품 신청 방법" in result["answer"]

    # Fallback 응답 상태를 확인한다.
    assert result["status"] == "excerpt"
