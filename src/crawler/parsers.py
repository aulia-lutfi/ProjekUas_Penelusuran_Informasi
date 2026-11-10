import re

from bs4 import BeautifulSoup

BULAN = r"januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember"
PAT_TANGGAL = re.compile(rf"\b\d{{1,2}}\s+(?:{BULAN})\s+\d{{4}}\b", re.IGNORECASE)
KATA_PERSYARATAN = re.compile(
    r"persyaratan|warga negara|ipk|berusia|usia|sarjana|bahasa inggris|sehat|minimal", re.IGNORECASE
)
KATA_BIAYA = re.compile(
    r"biaya|pembiayaan|tunjangan|uang saku|fasilitas|tuition|dibiayai|bantuan|fully funded|full funded",
    re.IGNORECASE,
)
KATA_TENGGAT = re.compile(
    r"batas|deadline|tenggat|paling lambat|dibuka sampai|sampai dengan", re.IGNORECASE
)


def extract_fields(isi):
    baris = [b.strip() for b in isi.split("\n") if b.strip()]

    persyaratan = [b for b in baris if KATA_PERSYARATAN.search(b)]
    pembiayaan = [b for b in baris if KATA_BIAYA.search(b)]

    tenggat = []
    for b in baris:
        if KATA_TENGGAT.search(b):
            tenggat.extend(PAT_TANGGAL.findall(b))

    return {
        "persyaratan": persyaratan,
        "pembiayaan": pembiayaan,
        "tenggat": tenggat,
    }


def parse_ditmawa(html, url, doc_id):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.select_one("h1.post-title")
    body_tag = soup.select_one("div.post-content")
    if title_tag is None or body_tag is None:
        return None

    for tag in body_tag.select("script, style"):
        tag.decompose()

    text = body_tag.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{2,}", "\n", text)

    doc = {
        "doc_id": doc_id,
        "url": url,
        "judul": title_tag.get_text(strip=True),
        "isi": text,
    }
    doc.update(extract_fields(text))
    return doc