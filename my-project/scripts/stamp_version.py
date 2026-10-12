"""Проставляет в experiment.md метку версии сборки.

Метка (хеш коммита, дата сборки UTC, md5 набора данных) вписывается
между маркерами BUILD-INFO-START/END, остальной текст страницы не трогается.
Запускается в CI перед mkdocs build; локально — через `make build`.
"""
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "experiment.csv"
PAGE_PATH = BASE_DIR / "docs" / "experiment.md"

START = "<!-- BUILD-INFO-START -->"
END = "<!-- BUILD-INFO-END -->"


def git_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=BASE_DIR, text=True,
        ).strip()
    except Exception:
        return "unknown"


def data_md5() -> str:
    return hashlib.md5(DATA_PATH.read_bytes()).hexdigest()[:10]


def main() -> None:
    raw = PAGE_PATH.read_bytes()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8")
    block = (
        f"{START}\n\n"
        "## Версия сборки\n\n"
        f"- Коммит: `{git_hash()}`\n"
        f"- Дата сборки (UTC): `{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}`\n"
        f"- Данные `experiment.csv` (md5): `{data_md5()}`\n\n"
        f"{END}\n"
    )
    if START in text and END in text:
        before, _, rest = text.partition(START)
        _, _, after = rest.partition(END)
        new_text = before + block + after
    else:
        new_text = text.rstrip() + "\n\n" + block
    if crlf:
        new_text = new_text.replace("\n", "\r\n")
    PAGE_PATH.write_bytes(new_text.encode("utf-8"))
    print("stamped version info into experiment.md")


if __name__ == "__main__":
    main()
