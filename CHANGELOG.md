# Changelog

## 1.0.0

The first release.

- The catalogue: 56 meme sounds, each with its title, length, source page, media URL, sha256,
  play count at collection, story with its source, what it usually marks, and its measured hit.
- `fetch.py`: downloads the recordings from their source pages and checks every sha256; three tries
  on a 15 s timeout, since the host stalls now and then.
- `hit.py`: measures a recording's head, arrival and length with ffmpeg alone.
- `cue.py`: lands a sound's hit on a second of a video or audio file.
- Four original CC0 sounds: a train, far dogs, a chime, a notice tone.
- `SKILL.md`: how to choose a sound for a moment and how to land it.

The repository ships no third-party audio.
