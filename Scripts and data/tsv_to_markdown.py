"""Convert "HSK list with meaning" TSVs (non-Anki) to Markdown tables.

Each source TSV has columns: traditional, simplified, pinyin, meaning.
We drop the traditional column and emit a Markdown table with a generated
row number so the lists are pleasant to read on a phone. The original .tsv
is removed once the .md is written.
"""

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "HSK list with meaning"
HEADERS = ["#", "Simplified", "Pinyin", "Meaning"]


def escape(cell: str) -> str:
    return cell.replace("|", "\\|")


def convert(tsv_path: Path) -> Path:
    rows = []
    for i, line in enumerate(tsv_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        _trad, simp, pinyin, meaning = line.split("\t", 3)
        rows.append([str(i), simp, pinyin, meaning])

    lines = [
        "| " + " | ".join(HEADERS) + " |",
        "| " + " | ".join(["---"] * len(HEADERS)) + " |",
    ]
    lines.extend("| " + " | ".join(escape(c) for c in row) + " |" for row in rows)

    md_path = tsv_path.with_suffix(".md")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path


def main() -> None:
    for tsv_path in sorted(SRC_DIR.glob("HSK *.tsv")):
        if tsv_path.name.startswith("Anki"):
            continue
        md_path = convert(tsv_path)
        tsv_path.unlink()
        print(f"{tsv_path.name} -> {md_path.name}")


if __name__ == "__main__":
    main()
