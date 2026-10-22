# 제2장 Python 기본 문법과 상품 데이터 처리

Python 3.12 및 uv 프로젝트. 제1장의 개발환경에서 이어서 실습한다. Django/MySQL은 이 장에서 사용하지 않는다.

## 처음부터 실행하기 (PowerShell)

```powershell
uv python install 3.12
uv sync
uv run python 01_variables.py
uv run python 02_calculate.py
uv run python 03_condition.py
uv run python 04_loop.py
uv run python 05_functions.py
uv run python catalog.py
uv run python 07_json.py
uv run python 08_exceptions.py
uv run python shop.py
uv run pytest -v
uv run python exercises/answers.py
```

`07_json.py` 실행 후 생성되는 `products.json`은 `.gitignore`에 의해 Git 추적에서 제외된다. 테스트는 pytest 8개이며 재고를 각 테스트 후 복원한다.
