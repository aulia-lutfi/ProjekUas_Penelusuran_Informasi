from pathlib import Path

import pandas as pd

from src.retrieval.search import Index

ROOT = Path(__file__).resolve().parents[2]
QUERIES = ROOT / "data" / "queries" / "queries.csv"
POOL = ROOT / "data" / "queries" / "pool.csv"

KUERI = [
    "beasiswa S2 luar negeri",
    "beasiswa S1 untuk mahasiswa berprestasi",
    "beasiswa KIP Kuliah",
    "beasiswa untuk mahasiswa Papua",
    "beasiswa tugas akhir",
    "beasiswa dari perusahaan",
    "beasiswa penelitian dan riset",
    "beasiswa pendidikan doktor",
    "beasiswa untuk mahasiswa tidak mampu",
    "beasiswa kepemimpinan",
    "beasiswa Jepang",
    "pendaftaran beasiswa dan batas waktu",
]


def main():
    idx = Index()
    qrows = []
    prow = []
    for i, q in enumerate(KUERI, 1):
        qid = f"Q{i:02d}"
        qrows.append({"query_id": qid, "query": q})
        pool = {}
        for alg, hasil in (("cosine", idx.cosine(q)), ("jaccard", idx.jaccard(q))):
            for doc, _ in hasil:
                pool.setdefault(doc, set()).add(alg)
        for doc, algs in pool.items():
            prow.append({
                "query_id": qid,
                "query": q,
                "doc_id": doc,
                "judul": idx.judul[doc],
                "url": idx.url[doc],
                "sumber": ",".join(sorted(algs)),
                "relevan": "",
            })

    pd.DataFrame(qrows).to_csv(QUERIES, index=False, encoding="utf-8")
    pd.DataFrame(prow).to_csv(POOL, index=False, encoding="utf-8")
    print("kueri:", len(qrows))
    print("baris pool:", len(prow))
    print("disimpan ke:", POOL)


if __name__ == "__main__":
    main()
