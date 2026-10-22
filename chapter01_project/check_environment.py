"""Django 개발환경 확인 스크립트."""

import sys

import django

# Python 3.12인지 확인한다.
assert sys.version_info[:2] == (3, 12), "Python 3.12가 필요합니다."

print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")
print(f"Django: {django.get_version()}")
