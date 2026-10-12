import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "experiment.csv"
OUTPUT_PATH = BASE_DIR / "docs" / "assets" / "result.png"
PAGE_PATH = BASE_DIR / "docs" / "experiment.md"

TABLE_START = "<!-- RESULTS-TABLE-START -->"
TABLE_END = "<!-- RESULTS-TABLE-END -->"


def is_up_to_date() -> bool:
    """True, если график новее данных (пересчёт не нужен)."""
    return (
        OUTPUT_PATH.exists()
        and OUTPUT_PATH.stat().st_mtime >= DATA_PATH.stat().st_mtime
    )


def update_table(data) -> None:
    """Сводная таблица по данным — в experiment.md между маркерами.

    Обновляется при каждом запуске (дёшево: чтение CSV), независимо от
    кэширования PNG: таблица всегда соответствует текущим данным.
    Остальной текст страницы не трогается (паттерн как в stamp_version.py).
    """
    rows = ["| Показатель | x | y |", "|---|---|---|"]
    for name in ("count", "mean", "min", "max"):
        if name == "count":
            rows.append(f"| n | {int(data['x'].count())} | {int(data['y'].count())} |")
        else:
            rows.append(
                f"| {name} | {getattr(data['x'], name)():.2f} "
                f"| {getattr(data['y'], name)():.2f} |"
            )
    block = f"{TABLE_START}\n\n" + "\n".join(rows) + f"\n\n{TABLE_END}\n"
    raw = PAGE_PATH.read_bytes()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8")
    if TABLE_START in text and TABLE_END in text:
        before, _, rest = text.partition(TABLE_START)
        _, _, after = rest.partition(TABLE_END)
        new_text = before + block + after
    else:
        new_text = text.rstrip() + "\n\n## Сводная таблица\n\n" + block
    if crlf:
        new_text = new_text.replace("\n", "\r\n")
    PAGE_PATH.write_bytes(new_text.encode("utf-8"))
    print("updated results table in experiment.md")


def main(force: bool = False) -> None:
    data = pd.read_csv(DATA_PATH)
    update_table(data)

    if not force and is_up_to_date():
        print("skip: up to date (result.png новее experiment.csv)")
        return

    plt.figure()
    plt.plot(data["x"], data["y"], marker="o")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Experimental results")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"regenerated: {OUTPUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="пересчитать принудительно")
    args = parser.parse_args()
    main(force=args.force)
