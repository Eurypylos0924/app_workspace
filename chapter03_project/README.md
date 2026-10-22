# 제3장: 모듈·예외·JSON 상품 관리

PowerShell에서 프로젝트 폴더로 이동한 뒤 실행한다.

```powershell
uv sync
uv run python main.py list
uv run python main.py search 키보드
uv run python main.py order 1 2
uv run python main.py list
uv run pytest -v
uv run python exercises/solutions.py
```

`order` 실행 시 `data/products.json`이 생성되며 재고가 저장된다. 반복 실습을 초기화하려면 해당 파일을 삭제한다.
`tests/conftest.py`는 pytest가 자동으로 로드하므로 직접 실행하지 않는다. Django와 MySQL은 이 장에서 사용하지 않는다.
