"""LLM Markdown을 XSS 방지 HTML로 렌더링한다."""
import re
from urllib.parse import unquote
import bleach
import markdown

ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "h1", "h2", "h3", "h4", "blockquote", "code", "pre", "a", "hr"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}


def render_markdown(text: str) -> str:
    """Markdown을 변환한 뒤 위험한 HTML을 제거한다."""
    html = markdown.markdown(text or "", extensions=["extra", "sane_lists", "nl2br"], output_format="html")
    return bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                        protocols=["http", "https", "mailto"], strip=True)


def readable_source(filename: str) -> str:
    """URL 인코딩 또는 #Uxxxx 형태의 한글 파일명을 읽기 쉽게 복원한다."""
    filename = unquote(str(filename or ""))
    def replace(match):
        try:
            return chr(int(match.group(1), 16))
        except ValueError:
            return match.group(0)
    return re.sub(r"#U([0-9a-fA-F]{4,6})", replace, filename, flags=re.IGNORECASE)
