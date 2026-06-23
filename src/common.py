"""Shared paths + a small cached HTTP getter for the Westbrook project."""
import os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROC = os.path.join(ROOT, "data", "processed")
OUT = os.path.join(ROOT, "outputs")
for d in (RAW, PROC, OUT):
    os.makedirs(d, exist_ok=True)

PLAYER = "westbru01"            # Russell Westbrook on Basketball-Reference
SEASON_END = 2017              # 2016-17 season (Basketball-Reference uses the end year)

# Known facts for the correctness gate (the whole point of this season):
KNOWN = dict(games=81, triple_doubles=42, ppg=31.6, rpg=10.7, apg=10.4)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def http_get(url, cache_name):
    """GET with an on-disk cache so re-runs are offline + don't hammer the site."""
    path = os.path.join(RAW, cache_name)
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    req = urllib.request.Request(url, headers=UA)
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    open(path, "w", encoding="utf-8").write(html)
    return html
