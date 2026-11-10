import csv
import hashlib
import sys
import time
import urllib.robotparser
from urllib.parse import urlparse

import requests

from config import BOT_NAME, RAW_DIR, REQUEST_DELAY_SECONDS, REQUEST_TIMEOUT_SECONDS, USER_AGENT

_robots_cache = {}
_last_request_time = 0.0


def _get_robots(url):
    parts = urlparse(url)
    base = f"{parts.scheme}://{parts.netloc}"
    if base not in _robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        try:
            rp.read()
        except Exception as e:
            print(f"[GAGAL] robots.txt tidak bisa dibaca dari {base}: {e}")
            rp = None
        _robots_cache[base] = rp
    return _robots_cache[base]


def is_allowed(url):
    rp = _get_robots(url)
    if rp is None:
        return False  # jika robots.txt tidak bisa dibaca, jangan crawl
    return rp.can_fetch(BOT_NAME, url)


def _polite_wait():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < REQUEST_DELAY_SECONDS:
        time.sleep(REQUEST_DELAY_SECONDS - elapsed)
    _last_request_time = time.time()


def fetch_html(url):
    if not is_allowed(url):
        print(f"[SKIP] Dilarang oleh robots.txt: {url}")
        return None
    _polite_wait()
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.RequestException as e:
        print(f"[GAGAL] Koneksi ke {url}: {type(e).__name__}")
        return None
    if resp.status_code != 200:
        print(f"[GAGAL] Status {resp.status_code}: {url}")
        return None
    return resp.text


def save_raw(url, html):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    doc_id = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
    (RAW_DIR / f"{doc_id}.html").write_text(html, encoding="utf-8")

    manifest = RAW_DIR / "manifest.csv"
    is_new = not manifest.exists()
    with manifest.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["doc_id", "url"])
        writer.writerow([doc_id, url])
    return doc_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pemakaian: python -m src.crawler.fetch <URL>")
        sys.exit(1)
    url = sys.argv[1]
    html = fetch_html(url)
    if html:
        doc_id = save_raw(url, html)
        print(f"Tersimpan: data/raw/{doc_id}.html ({len(html)} karakter)")