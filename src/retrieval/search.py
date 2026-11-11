import math
from collections import defaultdict
from pathlib import Path

import pandas as pd

from src.preprocessing.preprocess import _stem, _stopwords, tokenize

ROOT = Path(__file__).resolve().parents[2]
DOKUMEN = ROOT / "data" / "processed" / "dokumen.csv"
POSTINGS = ROOT / "data" / "processed" / "postings.csv"


class Index:
    def __init__(self):
        d = pd.read_csv(DOKUMEN, dtype=str).fillna("")
        self.judul = dict(zip(d.doc_id, d.judul))
        self.url = dict(zip(d.doc_id, d.url))
        self.N = len(d)

        p = pd.read_csv(POSTINGS, dtype={"stem": str, "doc_id": str})
        self.doc_terms = defaultdict(dict)
        self.df = defaultdict(int)
        for stem, doc, tf in zip(p.stem, p.doc_id, p.tf):
            self.doc_terms[doc][stem] = int(tf)
            self.df[stem] += 1

        self.idf = {s: math.log(self.N / df) for s, df in self.df.items()}
        self.norm = {}
        for doc, terms in self.doc_terms.items():
            self.norm[doc] = math.sqrt(sum(self._w(tf, s) ** 2 for s, tf in terms.items()))

    def _w(self, tf, stem):
        return (1 + math.log(tf)) * self.idf.get(stem, 0.0)

    def query_terms(self, teks):
        stop = _stopwords()
        return {_stem(t) for t in tokenize(teks) if t not in stop}

    def cosine(self, teks, k=10):
        q = defaultdict(int)
        stop = _stopwords()
        for t in tokenize(teks):
            if t not in stop:
                q[_stem(t)] += 1
        wq = {s: self._w(tf, s) for s, tf in q.items() if s in self.idf}
        norm_q = math.sqrt(sum(w * w for w in wq.values()))
        if norm_q == 0:
            return []

        skor = defaultdict(float)
        for s, w_q in wq.items():
            for doc, terms in self._postings_for(s):
                skor[doc] += w_q * self._w(terms[s], s)
        hasil = [(doc, v / (norm_q * self.norm[doc])) for doc, v in skor.items() if self.norm[doc] > 0]
        return sorted(hasil, key=lambda x: x[1], reverse=True)[:k]

    def _postings_for(self, stem):
        return [(doc, terms) for doc, terms in self.doc_terms.items() if stem in terms]

    def jaccard(self, teks, k=10):
        q = self.query_terms(teks)
        if not q:
            return []
        hasil = []
        for doc, terms in self.doc_terms.items():
            a = set(terms)
            irisan = len(q & a)
            if irisan:
                hasil.append((doc, irisan / len(q | a)))
        return sorted(hasil, key=lambda x: x[1], reverse=True)[:k]


def tampilkan(hasil, idx):
    for i, (doc, skor) in enumerate(hasil, 1):
        print(f"{i:2}. [{skor:.4f}] {idx.judul[doc]}")
        print(f"     {idx.url[doc]}")


if __name__ == "__main__":
    import sys

    idx = Index()
    kueri = " ".join(sys.argv[1:]) or "beasiswa S2 luar negeri"
    print("Kueri:", kueri)
    print("\n== Cosine (TF-IDF) ==")
    tampilkan(idx.cosine(kueri), idx)
    print("\n== Jaccard ==")
    tampilkan(idx.jaccard(kueri), idx)
