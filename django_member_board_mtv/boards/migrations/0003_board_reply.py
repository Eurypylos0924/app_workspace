"""MySQL의 중단된 0003 마이그레이션을 기존 데이터 보존 방식으로 복구한다.

DB에 이미 생성된 컬럼은 유지하며, Django migration state는 정확히 등록한다.
"""
from django.db import migrations, models
import django.db.models.deletion


def field_definitions():
    """마이그레이션 시점 모델에 아직 없는 필드를 독립적으로 정의한다."""
    return {
        "parent": models.ForeignKey("boards.Board", on_delete=django.db.models.deletion.CASCADE,
                                    null=True, blank=True, related_name="replies", verbose_name="부모 게시글"),
        "root_id": models.PositiveBigIntegerField("원글 ID", null=True, blank=True, db_index=True),
        "depth": models.PositiveIntegerField("답글 깊이", default=0),
        "thread_path": models.CharField("답글 정렬 경로", max_length=700, blank=True),
    }


def ensure_reply_columns(apps, schema_editor):
    """기존 컬럼을 유지하고 누락된 필드만 추가한다. 기존 필드의 타입은 변경하지 않는다."""
    Board = apps.get_model("boards", "Board")
    connection = schema_editor.connection
    table = Board._meta.db_table
    with connection.cursor() as cursor:
        columns = {col.name for col in connection.introspection.get_table_description(cursor, table)}
    for name, field in field_definitions().items():
        # 기존 컬럼이어도 모델에 먼저 등록해야 FK 및 인덱스 생성 시 ORM 상태가 일치한다.
        field.contribute_to_class(Board, name)
        if field.column not in columns:
            schema_editor.add_field(Board, field)
            columns.add(field.column)
    # 기존 컬럼이 일부 생성된 경우 누락된 root_id 인덱스도 보완한다.
    with connection.cursor() as cursor:
        constraints = connection.introspection.get_constraints(cursor, table)
    indexed_root = any(c.get("index") and "root_id" in c.get("columns", []) for c in constraints.values())
    if not indexed_root:
        schema_editor.add_index(Board, models.Index(fields=["root_id"], name="boards_reply_root_idx"))


def backfill_threads(apps, schema_editor):
    """기존 원글의 비어 있는 경로만 보정하며 답글의 parent 값은 보존한다."""
    Board = apps.get_model("boards", "Board")
    alias = schema_editor.connection.alias
    for board in Board.objects.using(alias).filter(parent__isnull=True).iterator():
        changes = {}
        if board.root_id is None:
            changes["root_id"] = board.pk
        if not board.thread_path:
            changes["thread_path"] = f"{board.pk:012d}"
        if changes:
            Board.objects.using(alias).filter(pk=board.pk).update(**changes)


class Migration(migrations.Migration):
    dependencies = [("boards", "0002_initial")]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[migrations.RunPython(ensure_reply_columns, migrations.RunPython.noop)],
            state_operations=[
                migrations.AddField("board", "parent", field_definitions()["parent"]),
                migrations.AddField("board", "root_id", field_definitions()["root_id"]),
                migrations.AddField("board", "depth", field_definitions()["depth"]),
                migrations.AddField("board", "thread_path", field_definitions()["thread_path"]),
            ],
        ),
        migrations.RunPython(backfill_threads, migrations.RunPython.noop),
    ]
