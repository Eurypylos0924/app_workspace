"""게시글 저장/삭제 후 ChromaDB 인덱스 동기화."""
import logging
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Board
logger = logging.getLogger(__name__)

def _sync(pk, deleted=False):
    try:
        from assistant_app.services.rag import delete_board, index_board
        if deleted:
            delete_board(pk)
        else:
            board = Board.objects.filter(pk=pk).first()
            if board:
                index_board(board)
            else:
                delete_board(pk)
    except Exception:
        logger.exception("게시글 ChromaDB 동기화 실패: id=%s", pk)

@receiver(post_save, sender=Board)
def board_saved(sender, instance, **kwargs):
    transaction.on_commit(lambda pk=instance.pk: _sync(pk))

@receiver(post_delete, sender=Board)
def board_deleted(sender, instance, **kwargs):
    transaction.on_commit(lambda pk=instance.pk: _sync(pk, deleted=True))
