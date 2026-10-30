#!/usr/bin/env python3
"""Measure where a recording hits: the instant that should land on the moment it is cued on.

    python3 scripts/hit.py FILE [FILE ...]      # head, arrival and length of each file
    python3 scripts/hit.py --sting FILE         # a sting that builds to its blow: the arrival is the hit

A soft head sits before the first sound of most recordings (0.13 s in the median across the catalogue,
up to 0.8 s). Start the file on the moment and the sound arrives that much late; centre it and a boom
lands early. So each sound has a HIT, measured on a 20 ms RMS envelope at 10 ms steps:

    head      the first instant above -40 dBFS: where the sound begins
    arrival   the first instant within 12 dB of the loudest: where it is fully there

For almost every sound the two are within a tenth of a second and the hit is the head. For a sting
that builds quietly to its blow the hit is the arrival, so the blow lands on the moment and the
build-up plays before it. Needs ffmpeg on the PATH; nothing else.
"""
import argparse
import array
import math
import subprocess
import sys

SR = 48000
HOP, WIN = SR // 100, SR // 50


def samples(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         check=True, capture_output=True).stdout
    x = array.array("h")
    x.frombytes(out[: len(out) - len(out) % 2])
    return x


def envelope_db(x):
    sq = [0.0]
    for v in x:
        sq.append(sq[-1] + (v / 32768.0) ** 2)
    db = []
    for i in range(0, max(1, len(x) - WIN), HOP):
        rms = math.sqrt((sq[i + WIN] - sq[i]) / WIN) + 1e-9
        db.append(20 * math.log10(rms))
    return db


def measure(path):
    x = samples(path)
    db = envelope_db(x)
    top = max(db)
    head = next((i for i, v in enumerate(db) if v > -40), 0) * HOP / SR
    arrival = next((i for i, v in enumerate(db) if v >= top - 12), 0) * HOP / SR
    return round(head, 2), round(arrival, 2), round(len(x) / SR, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--sting", action="store_true", help="the arrival is the hit")
    a = ap.parse_args()
    print("%-36s %6s %8s %7s %6s" % ("file", "head", "arrival", "length", "hit"))
    for f in a.files:
        try:
            head, arrival, length = measure(f)
        except subprocess.CalledProcessError as e:
            print("%-36s cannot decode: %s" % (f, e.stderr.decode().strip()), file=sys.stderr)
            continue
        print("%-36s %6.2f %8.2f %7.3f %6.2f" % (f[-36:], head, arrival, length, arrival if a.sting else head))


if __name__ == "__main__":
    main()
