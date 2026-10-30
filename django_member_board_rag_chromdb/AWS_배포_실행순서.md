# 개발/운영 Compose 분리

- `compose.yaml`: 첨부 원본과 동일, Windows 개발용 MySQL만 실행한다. 원본 포트 기본값은 3310이며 `.env`의 `MYSQL_PORT`가 우선한다.
- `compose.prod.yaml`: AWS Ubuntu용 MySQL + Django + Nginx. MySQL은 외부 포트를 열지 않는다.
- `config/settings.py`: STATIC_ROOT 및 운영용 HTTPS 환경변수를 추가하였다. 기존 DB 및 앱 구조는 유지한다.
- `.env`, `.venv`, DB 데이터 및 API 키는 이 패치에 포함하지 않는다.

## 적용
1. ZIP의 파일을 기존 프로젝트 루트에 병합한다. 기존 `compose.yaml`은 동일한 내용이다. `config/settings.py`를 별도로 수정한 이력이 있으면 비교 후 병합한다.
2. AWS의 `.env`에 MySQL 사용자/비밀번호, DJANGO_SECRET_KEY, OPENAI_API_KEY, DJANGO_ALLOWED_HOSTS를 설정한다. `MYSQL_PORT`는 개발용 호스트 포트이므로 AWS 컨테이너의 DB 접속에는 영향을 주지 않는다.
3. `docker compose -f compose.prod.yaml config --quiet`
4. `docker compose -f compose.prod.yaml up -d --build`
5. `docker compose -f compose.prod.yaml exec web .venv/bin/python manage.py check`
6. `docker compose -f compose.prod.yaml exec web .venv/bin/python manage.py migrate`
7. `docker compose -f compose.prod.yaml exec web .venv/bin/python manage.py createsuperuser`
8. `docker compose -f compose.prod.yaml exec web .venv/bin/python manage.py index_docs`
9. `docker compose -f compose.prod.yaml exec web .venv/bin/python manage.py index_boards`

## 개발환경
`docker compose -f compose.yaml up -d` 또는 `docker compose up -d`

## 주의
- 이 구성은 **HTTP 검증용**이다. 운영 공개 전 HTTPS/도메인/인증서와 Secure Cookie 설정을 완료한다.
- `media` 경로가 공개된다. 비공개 첨부파일이 있으면 접근 통제를 별도 구현한다.
- 기존 MySQL 데이터는 `mysql_prod_data`로 자동 이전되지 않는다. 백업/복원을 수행한다.
- `docker compose down -v`는 DB 볼륨을 삭제할 수 있으므로 실행하지 않는다.
- Gunicorn은 Docker 빌드 중 별도로 설치하며 uv.lock에는 추가하지 않는다. 배포 재현성을 높이려면 이후 프로젝트 의존성으로 고정한다.
