# meme-sounds-skill

An [Agent Skill](https://github.com/anthropics/skills) for Claude Code, Codex and the other agents that
read `SKILL.md`: pick a meme sound for a moment in a short video and land it on that moment.

Short-form video runs on a few dozen sounds everyone knows: the Vine boom on a reveal, bruh on a bad
idea, the wrong-answer buzzer, the sad violin, the Curb credits over a disaster. An agent cutting a
video needs three things it does not have: which sound means what, where to get the exact file, and
where in the file the hit is, so it lands on the cut instead of a quarter second after. This repository
is those three things.

## What is in it

- **The catalogue**, `skills/meme-sounds/catalog.yaml`: 56 sounds. Each has its title, length, the
  page that offers the MP3 and the file's sha256, the play count the page showed when it was collected,
  the sound's story with its source, what it usually marks, and its measured hit.
- **`fetch.py`**: brings the files to your machine from their source pages and checks every hash. The
  repository holds no third-party audio. The sounds belong to their owners, and the source site's terms
  allow personal use; whether one can go into a published video is the publisher's call.
- **`hit.py`**: measures where any recording hits (ffmpeg only, no Python packages).
- **`cue.py`**: puts a sound's hit on a second of a video or audio file.
- **Four original sounds** in `sounds/`, CC0: a train, far dogs, a chime, a notice tone.
- **`SKILL.md`**: how to choose a sound for a moment and how to land it.

## Install

```bash
npx skills add TravnikovDev/meme-sounds-skill
```

or copy `skills/meme-sounds/` into your project's `.claude/skills/` (Claude Code) or wherever your
agent reads skills from. The scripts need Python 3.9 or later and ffmpeg on the PATH; nothing else.

## Use

```bash
cd skills/meme-sounds
python3 scripts/fetch.py                                   # all 56 into fetched/
python3 scripts/cue.py cut.mp4 --cue vine-boom@3.20        # the boom's hit on 3.20 s
python3 scripts/cue.py cut.mp4 --cue bruh@7.9 --cue sad-violin@12.0 --gain -6
python3 scripts/hit.py own.mp3                             # head, arrival, length of your own file
```

## Why a hit, not a start

Nearly every recording carries a soft head before its first sound, 0.13 s in the median across the
catalogue and up to 0.8 s. Start the file on the moment and the sound arrives late. Centre it and a
boom whose hit sits 0.08 s into a 1.25 s file lands half a second early. So each entry has `hit_sec`,
the instant that should sit on the moment: the head for almost every sound, the blow for a sting that
builds to it. `cue.py` starts the file that much earlier.

## Where it comes from

The catalogue was built for [Rotville](https://github.com/TravnikovDev/Rotville), a channel of short
PS1-style cartoons, where every clip cues its sounds from a register like this one and a build tool
lands them on the moment. The hits were measured there and checked by ear in the finished clips.

## Licence

Code, the catalogue and its text: MIT. The four sounds in `sounds/`: CC0 1.0. The recordings the
catalogue describes: their owners'.
