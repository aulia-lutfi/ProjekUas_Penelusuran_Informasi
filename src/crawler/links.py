import re

from config import PROCESSED_DIR
from src.crawler.fetch import fetch_html

CATEGORY = "https://ditmawa.ugm.ac.id/category/info-beasiswa"
ARTICLE_RE = re.compile(r'https://ditmawa\.ugm\.ac\.id/\d{4}/\d{2}/[^"\s#?]+/')


def collect_links(max_pages):
    links = set()
    for page in range(1, max_pages + 1):
        url = CATEGORY if page == 1 else f"{CATEGORY}/page/{page}/"
        html = fetch_html(url)
        if html is None:
            print(f"Halaman {page}: dilewati")
            continue
        found = {u for u in ARTICLE_RE.findall(html) if not u.endswith("/feed/")}
        if not found:
            print(f"Halaman {page}: tidak ada artikel, berhenti")
            break
        links.update(found)
        print(f"Halaman {page}: {len(found)} tautan")
    return sorted(links)


if __name__ == "__main__":
    links = collect_links(max_pages=100)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR / "article_links.txt").write_text("\n".join(links), encoding="utf-8")
    print(f"Total {len(links)} tautan artikel unik")