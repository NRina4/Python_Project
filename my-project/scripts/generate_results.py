import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "experiment.csv"
OUTPUT_PATH = BASE_DIR / "docs" / "assets" / "result.png"


def is_up_to_date() -> bool:
    """True, если график новее данных (пересчёт не нужен)."""
    return (
        OUTPUT_PATH.exists()
        and OUTPUT_PATH.stat().st_mtime >= DATA_PATH.stat().st_mtime
    )


def main(force: bool = False) -> None:
    if not force and is_up_to_date():
        print("skip: up to date (result.png новее experiment.csv)")
        return

    data = pd.read_csv(DATA_PATH)

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
