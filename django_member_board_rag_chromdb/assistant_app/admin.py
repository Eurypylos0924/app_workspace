from django.contrib import admin
from .models import ChatMessage
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
 list_display=('session_key','role','agent','created_at')
 list_filter=('role','agent')
 search_fields=('session_key','content')
