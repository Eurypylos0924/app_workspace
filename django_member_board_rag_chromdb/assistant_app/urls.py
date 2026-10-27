from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="rag_home"), path("api/chat/", views.chat, name="rag_chat"), path("api/health/", views.health, name="rag_health")]
