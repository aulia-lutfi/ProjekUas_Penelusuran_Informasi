from pathlib import Path

import pandas as pd

from src.retrieval.search import Index

ROOT = Path(__file__).resolve().parents[2]
POOL = ROOT / "data" / "queries" / "pool.csv"
QUERIES = ROOT / "data" / "queries" / "queries.csv"
OUT = ROOT / "results" / "evaluasi.csv"


def metrik(ranking, relevan):
    k = len(ranking)
    hits = [d in relevan for d in ranking]
    tp = sum(hits)
    p = tp / k if k else 0.0
    r = tp / len(relevan) if relevan else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0

    benar, jumlah = 0, 0.0
    for i, h in enumerate(hits, 1):
        if h:
            benar += 1
            jumlah += benar / i
    ap = jumlah / len(relevan) if relevan else 0.0
    return p, r, f1, ap


def main():
    pool = pd.read_csv(POOL, dtype=str).fillna("")
    pool["relevan"] = pool["relevan"].str.strip()

    kosong = (pool["relevan"] == "").sum()
    if kosong:
        print(f"Belum dinilai: {kosong} dari {len(pool)} baris masih kosong di kolom 'relevan'.")
        return
    tidak_valid = (~pool["relevan"].isin(["0", "1"])).sum()
    if tidak_valid:
        print(f"Ada {tidak_valid} baris dengan nilai selain 0 atau 1 di kolom 'relevan'.")
        return

    idx = Index()
    queries = pd.read_csv(QUERIES, dtype=str)

    rows = []
    for qid, q in zip(queries["query_id"], queries["query"]):
        relevan = set(pool[(pool.query_id == qid) & (pool.relevan == "1")]["doc_id"])
        for alg, fn in (("Cosine", idx.cosine), ("Jaccard", idx.jaccard)):
            ranking = [doc for doc, _ in fn(q, k=10)]
            p, r, f1, ap = metrik(ranking, relevan)
            rows.append({
                "query_id": qid,
                "query": q,
                "algoritma": alg,
                "jumlah_relevan": len(relevan),
                "precision": round(p, 4),
                "recall": round(r, 4),
                "f1": round(f1, 4),
                "ap": round(ap, 4),
            })

    df = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8")

    print("Rata-rata per algoritma (MAP = rata-rata AP):")
    rata = df.groupby("algoritma")[["precision", "recall", "f1", "ap"]].mean().round(4)
    rata = rata.rename(columns={"ap": "MAP"})
    print(rata.to_string())
    print("\nDisimpan ke:", OUT)


if __name__ == "__main__":
    main()
