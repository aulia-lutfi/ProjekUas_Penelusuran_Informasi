import hashlib

from config import PROCESSED_DIR, RAW_DIR
from src.crawler.fetch import fetch_html, save_raw


def doc_id_for(url):
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:12]


def main():
    text = (PROCESSED_DIR / "article_links.txt").read_text(encoding="utf-8")
    links = [line.strip() for line in text.splitlines() if line.strip()]

    berhasil = gagal = sudah_ada = 0
    for i, url in enumerate(links, 1):
        if (RAW_DIR / f"{doc_id_for(url)}.html").exists():
            sudah_ada += 1
            continue
        html = fetch_html(url)
        if html is None:
            gagal += 1
            continue
        save_raw(url, html)
        berhasil += 1
        print(f"[{i}/{len(links)}] OK {url}")

    print(f"Berhasil: {berhasil}, gagal: {gagal}, sudah ada: {sudah_ada}")


if __name__ == "__main__":
    main()