#!/usr/bin/env python3
"""Land a sound's hit on a moment in a video or audio file.

    python3 scripts/cue.py IN.mp4 --cue vine-boom@3.20 [--cue bruh@7.9 ...] [--gain -6] [--out OUT.mp4]
    python3 scripts/cue.py IN.mp4 --cue path/to/own.mp3@3.20:0.12      # any file, its hit after the colon

A cue is <sound>@<seconds>: the sound's HIT lands on that second, so the file starts hit_sec earlier
(or its head is cut when the moment is nearer the start than the hit). A catalogue id looks in fetched/
(run scripts/fetch.py first); a path is used as it is, with the hit after a colon, 0 when none. --gain
is in dB on every cue. The video stream is copied; the mix is the input's own audio with the cues over
it, nothing normalised down. Needs ffmpeg on the PATH; nothing else.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent


def resolve(spec):
    name, _, at = spec.rpartition("@")
    hit = 0.0
    if ":" in at:
        at, hit = at.split(":", 1)
        hit = float(hit)
    at = float(at)
    p = Path(name)
    if p.is_file():
        return p, at, hit
    sounds = {s["id"]: s for s in json.loads((SKILL / "catalog.json").read_text())["sounds"]}
    if name not in sounds:
        sys.exit("%s is neither a file nor a catalogue id" % name)
    p = SKILL / "fetched" / (name + ".mp3")
    if not p.is_file():
        sys.exit("%s is not fetched yet: python3 scripts/fetch.py %s" % (name, name))
    return p, at, float(sounds[name]["hit_sec"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("input")
    ap.add_argument("--cue", action="append", required=True, help="<id or file>@<seconds>[:<hit>]")
    ap.add_argument("--gain", type=float, default=0.0, help="dB on every cue")
    ap.add_argument("--out", help="default: <input>.cued.<ext>")
    a = ap.parse_args()
    src = Path(a.input)
    out = Path(a.out) if a.out else src.with_name(src.stem + ".cued" + src.suffix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src)]
    chains = []
    for k, spec in enumerate(a.cue, 1):
        path, at, hit = resolve(spec)
        cmd += ["-i", str(path)]
        start = at - hit
        place = "adelay=%d:all=1" % round(start * 1000) if start >= 0 else "atrim=start=%.3f,asetpts=PTS-STARTPTS" % -start
        chains.append("[%d:a]%s,volume=%.1fdB[c%d]" % (k, place, a.gain, k))
        print("  %-28s hit %.2f s on %.2f s, file from %.2f s" % (path.name, hit, at, start))
    n = len(a.cue)
    fc = ";".join(chains) + ";[0:a]" + "".join("[c%d]" % k for k in range(1, n + 1)) + "amix=inputs=%d:duration=first:normalize=0[a]" % (n + 1)
    cmd += ["-filter_complex", fc, "-map", "0:v?", "-map", "[a]", "-c:v", "copy"]
    if src.suffix.lower() in (".mp4", ".mov", ".m4a"):
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    cmd.append(str(out))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr.strip())
    print("wrote", out)


if __name__ == "__main__":
    main()
