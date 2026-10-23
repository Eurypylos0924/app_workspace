#!/usr/bin/env python
"""Django 관리 명령어를 실행하는 프로젝트 진입점이다."""
import os
import sys

def main():
    # config/settings.py를 Django 설정 파일로 지정한다.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # 명령줄 인수(runserver, migrate 등)를 Django에 전달한다.
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
