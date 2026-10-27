from django.core.management.base import BaseCommand
from assistant_app.services.rag import index_pdfs


class Command(BaseCommand):
    help = "PDF 문서만 text-embedding-3-small로 ChromaDB에 색인한다."

    def handle(self, *args, **options):
        docs = index_pdfs()
        self.stdout.write(self.style.SUCCESS(f"PDF 색인 완료: {docs}개 청크"))
