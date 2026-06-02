# Agent Instructions (Meetings)

This directory organizes Discord meeting recordings (captured with **Craig**) and the
artifacts derived from them: a combined, speaker-attributed transcript and a team-facing
summary.

The pipeline has four stages:

```
ingest  ->  transcribe  ->  merge  ->  summarize
```

The first three are mechanical and handled by the `meetings/tools/meeting` tool. The
**summarize** step is done by the agent reading the combined transcript (see below).

## How Craig recordings work

Craig records **one audio file per participant**, named `<n>-<discordusername>.<ext>`
(e.g. `7-captainkraft.flac`). All tracks share the same start time (t=0).

Because every track is a single speaker, **attribution is exact** — there is no need for
diarization or guessing the loudest speaker from a mixdown. We transcribe each track on
its own, tag every segment with that track's speaker, and merge by timestamp.

When downloading from Craig:

- Choose **Multi-track → FLAC** (one lossless file per speaker, small download).
- Do **not** use the Single-track (mixed) formats — they discard speaker separation.
- Do **not** use the Audacity/Audition project formats — they are not plain audio.
- Leave **normalize off**. We level quiet tracks in-pipeline only if needed, so the
  source stays clean (normalize can amplify a silent track's noise floor and cause
  hallucinated text).

## One-time setup

```bash
python3 -m venv meetings/tools/.venv
meetings/tools/.venv/bin/pip install -r meetings/tools/requirements.txt
```

This installs `faster-whisper` (CTranslate2 backend, no PyTorch). Models download on
first use and are cached under `~/.cache/huggingface`. `ffmpeg`/`ffprobe` are also used.

## Running the tool

Use the wrapper, which runs the script with the tool's venv:

```bash
# Full pipeline from a Craig multi-track zip:
meetings/tools/meeting all ~/Downloads/craig-xxxxxxxx.zip --date 2026-06-02 --title dev-team

# Or run stages individually against an existing meeting folder:
meetings/tools/meeting ingest ~/Downloads/craig-xxxxxxxx.zip --date 2026-06-02 --title dev-team
meetings/tools/meeting transcribe meetings/2026/2026-06-02_dev-team
meetings/tools/meeting merge      meetings/2026/2026-06-02_dev-team
```

Stages:

- `ingest <zip|dir>` — unzips a Craig multi-track download into a dated meeting folder
  and lays out `audio/`, `transcripts/`, `notes/`. Ignores non-track files
  (`combined.*`, project files). Accepts `--date` (default: today) and `--title`.
- `transcribe <meeting-dir>` — runs faster-whisper with VAD on each track and writes
  `transcripts/tracks/<n>-<user>.json`. Caches results: a track is skipped if its JSON
  is newer than the audio and used the same model. Use `--force` to re-run.
- `merge <meeting-dir>` — combines the per-track JSON into `transcripts/combined.md`
  (human-readable) and `transcripts/combined.json` (structured), sorted chronologically.
- `all <zip|dir|meeting-dir>` — ingest (if needed) → transcribe → merge.

Useful flags on `transcribe`/`all`:

- `--model` (default `small.en`) — use `medium.en` for higher accuracy if a meeting is
  important or has hard audio. Larger models are slower on CPU.
- `--language` (default `en`) — pass `auto` to detect per track.
- `--force` — re-transcribe even if a cached track JSON exists.

## Directory layout

Meetings are organized by date:

```
meetings/YYYY/YYYY-MM-DD_<title>/
  audio/         # per-speaker Craig tracks: <n>-<user>.flac
  transcripts/
    tracks/      # one JSON per track (intermediate)
    combined.md  # chronological, speaker-attributed transcript
    combined.json
  notes/
    summary.md   # team-facing summary (written by the agent)
```

Do not rename source audio files — the `<n>-<user>` names are how speakers are detected.

## Name mapping (`meetings/people.json`)

`people.json` maps a Discord username (lowercased) to a display name. Unmapped users
appear under their raw Discord username, and the tool prints a note listing them.

When you see unmapped users, ask who they are and add them to `people.json` — that file
is the single source of truth for the mapping. (Discord usernames differ from the GitHub
logins in `gh/AGENTS.md`, so the two maps are maintained separately.)

## Glossary (`meetings/glossary.md`)

`glossary.md` holds canonical spellings of JangaFX product names, people, and jargon, plus
the common speech-to-text mis-hearings (e.g. "Illusion" → IlluGen, "Liquid Gen" → LiquiGen,
"Morton" → Morten). The summary step uses it to fix ASR errors. Keep it growing as new team
terms come up.

## Combined transcript format

`combined.md` uses one block per utterance:

```
[HH:MM:SS] **Name:** spoken text
```

Consecutive segments from the same speaker within a couple of seconds are merged into one
block for readability. The raw file is meant to read cleanly on its own.

## Writing the summary (agent step)

When asked to summarize a meeting:

1. Read `transcripts/combined.md`.
2. Apply `meetings/glossary.md`: the raw transcript has speech-to-text errors, so correct
   mis-heard product names, people, and jargon to their canonical spellings (e.g. EmberGen,
   IlluGen, LiquiGen, Morten, Combustion Lab). Add any new team terms you discover.
3. Write `notes/summary.md` using `meetings/templates/summary.md` — keep its fixed
   headings: Overview, Key Decisions, Action Items, Discussion by Topic, Open Questions.
4. Attribute each action item to a named owner (`Owner — task — due`); include a due date
   only if one was actually stated.
5. Be faithful to the transcript. Do not invent decisions or outcomes. If something was
   left unresolved, put it under Open Questions rather than guessing.
6. For a long meeting whose transcript is too large to summarize in one pass, summarize it
   in time-ordered chunks, then combine those into the final summary (map-reduce). Keep
   the section structure consistent.

## Safety / constraints

- Local-first. Prefer local tooling and local file operations.
- Do **not** upload meeting audio or transcripts to external services unless the user
  explicitly asks. Note: asking the in-session agent to summarize necessarily sends the
  transcript to the model provider — that is expected when you request a summary, but do
  not push audio or transcripts anywhere else. For a fully offline summary, a local model
  would be needed instead.
- Keep the raw Markdown transcript and summary clean and readable outside any app.

## Example invocations

- `meetings/tools/meeting all ~/Downloads/craig-abc123.zip --date 2026-06-02 --title dev-team`
- `transcribe meetings/2026/2026-06-02_dev-team` (re-run with `--model medium.en` for accuracy)
- `summarize meetings/2026/2026-06-02_dev-team/transcripts/combined.md`
