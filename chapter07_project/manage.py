# Django 명령을 실행하는 진입점입니다.
import os
import sys


def main():
    # 어떤 설정 파일을 쓸지 지정합니다.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
