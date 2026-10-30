---
name: meme-sounds
description: Pick a meme sound for a moment in a short video and land it on that moment. A catalogue of 56 recordings short-form video reaches for (Vine boom, bruh, the wrong-answer buzzer, the sad violin), each with its story, what it usually marks, and its measured hit; a fetcher that brings the files to the machine; a cue tool that puts the hit on the second. Use when editing a video, scripting one with sound cues, or asked which sound fits a beat.
---

# Meme sounds

A meme sound is an audio cue the viewer already knows. It tells them how to take the moment: a reveal,
a failure, a flex, a sudden sadness, a creature walking in. Used on the right moment it does the work
of a caption; used on the wrong one it is noise. This skill is for choosing the sound and landing it.

## Files

- `catalog.yaml`: the sounds, one entry each, for people. `catalog.json` is the same content for the
  scripts. Fields: `id`, `title`, `duration_sec`, `hit_sec`, `source_page`, `media_url`, `sha256`,
  `views_at_collection`, `story`, `story_source`, `common_use`.
- `scripts/fetch.py`: downloads the recordings from their source pages into `fetched/` and checks
  each sha256. The repository holds no third-party audio.
- `scripts/hit.py`: measures a recording's hit, for a sound that is not in the catalogue.
- `scripts/cue.py`: lands a sound's hit on a second of a video or audio file, with ffmpeg.
- `sounds/`: four original sounds made for this repository, CC0, usable as they are.

## Choosing

1. Name the moment before the sound: what happens on screen, and what the viewer should feel about it.
   Reveal, fail, flex, dread, relief, a thing walking in, a long silence breaking.
2. Search `common_use` in the catalogue for that moment, then read the `story`. A sound carries its
   history: the Curb credits say "this went badly and everyone knows it", the Taco Bell bong says "a
   decision was just made". Use a sound whose meaning the viewer will bring with them.
3. One sound per turn. A beat gets one cue, and a clip of fifteen seconds rarely wants more than two
   or three. A sound on every line is a soundboard, not an edit.
4. No sound where the moment does not ask for one. Silence before a hit makes the hit.
5. Short sounds for cuts, long ones for a section: `duration_sec` says which. A 20 s song is a bed
   under a run of shots, never a sting.

## Landing

The cue's time is the moment, and the sound's HIT is what lands on it. Most recordings carry a soft
head before their first sound (0.13 s in the median, up to 0.8 s); starting the file on the moment
puts the sound late, and centring it puts a boom early. `hit_sec` is the measured instant: the head
for nearly every sound, the blow for a sting that builds to it. `cue.py` starts the file `hit_sec`
before the moment, so the hit sits on the second you name.

```bash
python3 scripts/fetch.py vine-boom bruh
python3 scripts/cue.py cut.mp4 --cue vine-boom@3.20 --cue bruh@7.90 --gain -6
```

For a sound of your own, measure it first and give the hit after a colon:

```bash
python3 scripts/hit.py own.mp3
python3 scripts/cue.py cut.mp4 --cue own.mp3@3.20:0.12
```

A boom belongs on its cut, within a frame. Listen once with the picture: if the sound seems to come
after the moment, the hit is late, not the moment early.

## Rights

The catalogue is data about recordings that belong to other people. Each entry names the page that
offers the file, and `fetch.py` downloads it to your machine under that site's terms, which allow
personal use. Whether a sound can go into a published, monetised video is the publisher's call, and a
famous sound is not a free one: the Vine boom is a licensed sample library's impact. The four files in
`sounds/` are the only audio in the repository and are CC0.
