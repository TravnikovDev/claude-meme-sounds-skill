#!/usr/bin/env python3
"""Fetch the catalogue's recordings to your machine and check each one against its sha256.

    python3 scripts/fetch.py                  # every sound into fetched/ beside the catalogue
    python3 scripts/fetch.py vine-boom bruh   # only these
    python3 scripts/fetch.py --to DIR         # into another folder
    python3 scripts/fetch.py --check          # report what is there and whether it matches, download nothing

A file whose sha256 already matches is left alone. One that downloads with another hash is kept with
.mismatch on its name and reported: the page changed its file, so listen before you use it.
"""
import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CATALOG = SKILL / "catalog.json"
FETCHED = SKILL / "fetched"
AGENT = "meme-sounds-skill/1.0 (+https://github.com/TravnikovDev/meme-sounds-skill)"


def catalog():
    return json.loads(CATALOG.read_text())["sounds"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r, open(tmp, "wb") as f:
                f.write(r.read())
            tmp.rename(dest)
            return True
        except Exception as e:  # noqa: BLE001 - report and retry once
            if attempt == 2:
                print("  %s: %s" % (url, e))
                tmp.unlink(missing_ok=True)
                return False
            time.sleep(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ids", nargs="*", help="sound ids; none means all")
    ap.add_argument("--to", type=Path, default=FETCHED, help="folder for the files (default: fetched/)")
    ap.add_argument("--check", action="store_true", help="report only; download nothing")
    a = ap.parse_args()
    sounds = catalog()
    if a.ids:
        known = {s["id"] for s in sounds}
        bad = [i for i in a.ids if i not in known]
        if bad:
            sys.exit("not in the catalogue: " + ", ".join(bad))
        sounds = [s for s in sounds if s["id"] in a.ids]
    a.to.mkdir(parents=True, exist_ok=True)
    ok = missing = changed = 0
    for s in sounds:
        dest = a.to / (s["id"] + ".mp3")
        if dest.is_file() and sha256(dest) == s["sha256"]:
            ok += 1
            continue
        if a.check:
            print("  %-28s %s" % (s["id"], "missing" if not dest.is_file() else "HASH DIFFERS"))
            missing += 1
            continue
        urls = [s["media_url"]] + ([s["alternate_media_url"]] if s.get("alternate_media_url") else [])
        got = False
        for url in urls:
            if not download(url, dest):
                continue
            if sha256(dest) == s["sha256"]:
                got = True
                break
            dest.rename(dest.with_suffix(".mp3.mismatch"))
        if got:
            ok += 1
            print("  %-28s fetched" % s["id"])
        elif dest.with_suffix(".mp3.mismatch").is_file():
            changed += 1
            print("  %-28s HASH DIFFERS from the catalogue, kept as %s" % (s["id"], dest.with_suffix(".mp3.mismatch").name))
        else:
            missing += 1
            print("  %-28s not fetched" % s["id"])
        time.sleep(0.5)
    print("%d match, %d missing, %d changed, in %s" % (ok, missing, changed, a.to))
    sys.exit(1 if (missing or changed) else 0)


if __name__ == "__main__":
    main()
