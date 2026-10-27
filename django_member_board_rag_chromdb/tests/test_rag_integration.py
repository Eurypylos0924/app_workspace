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
    assert result["agent"] == "rag"
    assert "게시글 #1" in result["answer"]
