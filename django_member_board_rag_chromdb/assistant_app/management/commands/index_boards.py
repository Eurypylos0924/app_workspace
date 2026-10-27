from django.core.management.base import BaseCommand
from assistant_app.services.rag import index_boards

class Command(BaseCommand):
    help = "게시글과 답글을 ChromaDB에 전체 색인한다."
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"게시글 청크 {index_boards()}건 색인 완료"))
