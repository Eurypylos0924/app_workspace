from django.db import migrations,models
class Migration(migrations.Migration):
 initial=True
 dependencies=[]
 operations=[migrations.CreateModel(name='ChatMessage',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),('session_key',models.CharField(max_length=64,db_index=True)),('role',models.CharField(max_length=12)),('content',models.TextField()),('agent',models.CharField(max_length=24,blank=True)),('created_at',models.DateTimeField(auto_now_add=True))],options={'ordering':['id']})]
