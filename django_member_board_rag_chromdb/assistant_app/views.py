"""Django chat API with server-side exception logging."""
import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import ChatMessage
from .services.agent import answer
from .utils.markdown_utils import render_markdown, readable_source

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def home(request):
    return render(request, "assistant_app/home.html")

def health(request):
    return JsonResponse({"status": "ok"})

@require_POST
def chat(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON 형식 오류"}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "JSON 객체를 입력해야 한다."}, status=400)
    message = payload.get("message", "")
    if not isinstance(message, str) or not message.strip() or len(message) > 3000:
        return JsonResponse({"error": "질문은 1~3000자로 입력해야 한다."}, status=400)
    try:
        if not request.session.session_key:
            request.session.create()
        sid = request.session.session_key
        history = list(ChatMessage.objects.filter(session_key=sid).order_by("-id")[:6].values("role", "content"))[::-1]
        result = answer(message.strip(), history)
        ChatMessage.objects.create(session_key=sid, role="user", content=message.strip())
        ChatMessage.objects.create(session_key=sid, role="assistant", content=result["answer"], agent=result["agent"])
        # 원본 answer는 기존 API 호환성을 위해 유지한다.
        response_data = dict(result)
        response_data["answer_html"] = render_markdown(result["answer"])
        response_data["sources"] = [
            {**source, "display_source": readable_source(source.get("source", ""))}
            for source in result.get("sources", [])
        ]
        return JsonResponse(response_data)
    except Exception:
        logger.exception("질문 처리 실패: message=%r", message[:100])
        return JsonResponse({"error": "서버 처리 오류가 발생했다. 서버 로그를 확인해야 한다."}, status=500)
