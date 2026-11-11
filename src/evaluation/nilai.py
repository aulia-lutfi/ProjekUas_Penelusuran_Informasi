from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
POOL = ROOT / "data" / "queries" / "pool.csv"


def main():
    p = pd.read_csv(POOL, dtype=str).fillna("")
    belum = p.index[p.relevan.str.strip() == ""].tolist()
    print(f"Belum dinilai: {len(belum)} dari {len(p)}")
    print("Ketik 1 (relevan), 0 (tidak), atau q (berhenti dan simpan).\n")

    for n, i in enumerate(belum, 1):
        r = p.loc[i]
        print(f"[{n}/{len(belum)}] Kueri: {r['query']}")
        print(f"    Judul: {r['judul']}")
        print(f"    URL  : {r['url']}")
        while True:
            jawab = input("    Relevan? (1/0/q): ").strip()
            if jawab in ("0", "1", "q"):
                break
            print("    Masukkan 1, 0, atau q.")
        if jawab == "q":
            break
        p.loc[i, "relevan"] = jawab
        p.to_csv(POOL, index=False, encoding="utf-8")
        print()

    p.to_csv(POOL, index=False, encoding="utf-8")
    print("Tersimpan. Sisa belum dinilai:", (p.relevan.str.strip() == "").sum())


if __name__ == "__main__":
    main()
