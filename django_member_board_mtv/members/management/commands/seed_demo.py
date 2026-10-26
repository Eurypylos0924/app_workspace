"""수업 실습용 관리자/일반회원/게시글 데이터를 생성하는 관리 명령입니다."""
from django.core.management.base import BaseCommand
from members.models import Member
from boards.models import Board

# Django가 manage.py <파일명> 실행 시 아래 Command 클래스를 자동으로 찾아 실행합니다.
class Command(BaseCommand):
    """python manage.py seed_demo 명령을 구현합니다."""
    help = "admin, user01, user02와 예제 게시글을 생성합니다."

    def handle(self, *args, **options):
        """중복 실행해도 기존 계정을 재사용하도록 데모 데이터를 생성합니다."""
        # 실행할 작업 작성
        self.stdout.write(self.style.SUCCESS("데모 데이터 생성 시작"))

        # 1. 관리자 계정 (admin / admin1234!)
        admin, created = Member.objects.get_or_create(
            username="admin",
            defaults={
                "display_name": "admin",
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            admin.set_password("admin1234!")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' 생성 완료"))
        else:
            self.stdout.write(self.style.WARNING("User 'admin' 이미 존재"))

        # 2. 일반회원 user01 (pass1234!)
        user01, created = Member.objects.get_or_create(
            username="user01",
            defaults={
                "display_name": "홍길동",
                "email": "user01@example.com",
                "gender": "M",
                "age": 30
            }
        )
        if created:
            user01.set_password("pass1234!")
            user01.save()
            self.stdout.write(self.style.SUCCESS("User 'user01' 생성 완료"))
        else:
            self.stdout.write(self.style.WARNING("User 'user01' 이미 존재"))

        # 3. 일반회원 user02 (pass1234!)
        user02, created = Member.objects.get_or_create(
            username="user02",
            defaults={
                "display_name": "김영희",
                "email": "user02@example.com",
                "gender": "F",
                "age": 28
            }
        )
        
        if created:
            user02.set_password("pass1234!")
            user02.save()
            self.stdout.write(self.style.SUCCESS("User 'user02' 생성 완료"))
        else:
            self.stdout.write(self.style.WARNING("User 'user02' 이미 존재"))

        # 4. 초기 예제 게시글 생성
        if not Board.objects.exists():
            Board.objects.create(author=admin, title="관리자 게시글 - MySQL 8.4 연동 완료", content="Docker MySQL 8.4 (포트 3309)와 연동된 Django MTV 커뮤니티입니다.")
            Board.objects.create(author=user01, title="uv 및 Python 3.12 실습", content="uv 패키지 매니저를 통해 빠른 가상환경 구축과 마이그레이션을 완료했습니다.")
            Board.objects.create(author=user02, title="회원 인증 및 게시판 기능", content="세션 기반 회원 인증, 권한 관리, 게시판 CRUD가 정상 작동합니다.")
            self.stdout.write(self.style.SUCCESS("초기 게시글 3건 생성 완료"))

        self.stdout.write(self.style.SUCCESS("데모 데이터 생성 완료: admin(admin1234!), user01(pass1234!), user02(pass1234!)"))
