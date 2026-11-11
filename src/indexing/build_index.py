from collections import Counter
from pathlib import Path

import pandas as pd

from src.preprocessing.preprocess import _stopwords, tokenize

ROOT = Path(__file__).resolve().parents[2]
DOKUMEN = ROOT / "data" / "processed" / "dokumen.csv"
STEM_MAP = ROOT / "data" / "processed" / "stem_map.csv"
POSTINGS = ROOT / "data" / "processed" / "postings.csv"
PANJANG = ROOT / "data" / "processed" / "doc_length.csv"


def main():
    d = pd.read_csv(DOKUMEN).fillna("")
    peta_df = pd.read_csv(STEM_MAP, dtype=str, keep_default_na=False)
    peta = dict(zip(peta_df.token, peta_df.stem))
    stop = _stopwords()

    postings = []
    panjang = []
    for doc_id, judul, isi in zip(d.doc_id, d.judul, d.isi):
        tokens = [t for t in tokenize(judul + " " + isi) if t not in stop]
        hitung = Counter(peta[t] for t in tokens)
        panjang.append({"doc_id": doc_id, "panjang": sum(hitung.values())})
        postings.extend({"stem": s, "doc_id": doc_id, "tf": f} for s, f in hitung.items())

    pd.DataFrame(postings).to_csv(POSTINGS, index=False, encoding="utf-8")
    pd.DataFrame(panjang).to_csv(PANJANG, index=False, encoding="utf-8")

    print("dokumen:", len(d))
    print("baris postings:", len(postings))
    print("stem unik:", len({p["stem"] for p in postings}))
    print("disimpan ke:", POSTINGS)


if __name__ == "__main__":
    main()
