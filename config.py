from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
QUERIES_DIR = ROOT_DIR / "data" / "queries"
RESULTS_DIR = ROOT_DIR / "results"

BOT_NAME = "PI-Kelompok1-Crawler"
USER_AGENT = f"{BOT_NAME}/1.0 (tugas kuliah; kontak: aulialtfi18@gmail.com)"
REQUEST_DELAY_SECONDS = 3
REQUEST_TIMEOUT_SECONDS = 15
TOP_K = 10