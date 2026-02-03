# Agent Instructions (Meetings)

This directory is for organizing meeting recordings and their derived artifacts (transcripts, summaries, notes).
Each meeting will have multiple tracks, one for each participant. The goal will be to transcribe all tracks
into a combined transcript and then produce a separate summary document that can be given to the team
to keep as notes.

## Safety / constraints

- Do not send meeting audio or full transcripts to external services unless the user explicitly requests it.
- Prefer local tooling and local file operations.
- Use local `ffmpeg` for mixdowns and the `whisper` CLI for transcription when needed.
- Combined transcripts should include speaker names by aligning the timecoded mixdown transcript with per-track audio levels (use RMS/volume to pick the loudest speaker per segment).

## Directory layout

- Meetings are organized by date:
  - `meetings/YYYY/YYYY-MM-DD_<optional-title>/`

Recommended subfolders inside each meeting folder:
- `audio/` (source audio; may include multi-track exports)
- `audacity/` (Audacity projects: `.aup3` and any related folders)
- `transcripts/` (raw or lightly processed transcripts: `.txt`, `.srt`, `.vtt`, `.json`)
- `notes/` (human-written notes and summaries)

## File handling conventions

- Prefer **no renames** when organizing existing files; only move them into the correct folder.
- If a meeting folder currently has loose audio/transcript files, place them into the subfolders above.

## Example invocations

- `organize this meeting folder`
- `transcribe meetings/2025/2025-01-15/audio/foo.wav`
- `summarize meetings/2025/2025-01-15/transcripts/combined.txt`
- `make a short action-items list from the transcript`
