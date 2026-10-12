from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "experiment.csv"
OUTPUT_PATH = BASE_DIR / "docs" / "assets" / "result.png"


def main() -> None:
    data = pd.read_csv(DATA_PATH)

    plt.figure()
    plt.plot(data["x"], data["y"], marker="o")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Experimental results")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
