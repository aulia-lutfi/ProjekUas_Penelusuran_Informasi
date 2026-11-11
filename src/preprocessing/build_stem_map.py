from pathlib import Path

import pandas as pd

from src.preprocessing.preprocess import _stem, _stopwords, tokenize

ROOT = Path(__file__).resolve().parents[2]
DOKUMEN = ROOT / "data" / "processed" / "dokumen.csv"
OUT = ROOT / "data" / "processed" / "stem_map.csv"


def main():
    d = pd.read_csv(DOKUMEN).fillna("")
    stop = _stopwords()

    unik = set()
    for judul, isi in zip(d.judul, d.isi):
        unik.update(t for t in tokenize(judul + " " + isi) if t not in stop)

    print("kata unik:", len(unik))

    peta = pd.DataFrame({"token": sorted(unik)})
    peta["stem"] = [_stem(t) for t in peta["token"]]
    peta.to_csv(OUT, index=False, encoding="utf-8")

    print("disimpan ke:", OUT)
    print("jumlah baris:", len(peta))


if __name__ == "__main__":
    main()
