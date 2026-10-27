from django.db import models
class ChatMessage(models.Model):
 session_key=models.CharField(max_length=64,db_index=True)
 role=models.CharField(max_length=12)
 content=models.TextField()
 agent=models.CharField(max_length=24,blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:
  ordering=['id']
