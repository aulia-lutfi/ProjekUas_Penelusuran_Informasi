from pathlib import Path

import pandas as pd

from src.crawler.parsers import parse_ditmawa

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "manifest.csv"
OUT = ROOT / "data" / "processed" / "dokumen.csv"


def main():
    manifest = pd.read_csv(MANIFEST).drop_duplicates(subset="doc_id")
    rows = []
    hilang = 0
    bukan_artikel = 0

    for _, r in manifest.iterrows():
        path = RAW / f"{r.doc_id}.html"
        if not path.exists():
            hilang += 1
            continue

        html = path.read_text(encoding="utf-8", errors="replace")
        doc = parse_ditmawa(html, r.url, r.doc_id)
        if doc is None:
            bukan_artikel += 1
            continue

        rows.append({
            "doc_id": doc["doc_id"],
            "url": doc["url"],
            "judul": doc["judul"],
            "isi": doc["isi"],
            "persyaratan": " | ".join(doc["persyaratan"]),
            "pembiayaan": " | ".join(doc["pembiayaan"]),
            "tenggat": " | ".join(doc["tenggat"]),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8")

    print(f"Dokumen valid: {len(rows)}")
    print(f"Bukan artikel (dilewati): {bukan_artikel}")
    print(f"File HTML tidak ditemukan: {hilang}")
    print(f"Disimpan ke: {OUT}")


if __name__ == "__main__":
    main()