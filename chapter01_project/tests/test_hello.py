"""hello.py 실행 결과 확인."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hello_output():
    # 프로젝트 루트의 hello.py를 실행한다.
    script = ROOT / "hello.py"
    assert script.is_file(), f"파일이 없습니다: {script}"

    # 현재 uv 가상환경의 Python으로 실행한다.
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "프로젝트: chapter01-development" in result.stdout
    assert "Python 버전: 3.12" in result.stdout
