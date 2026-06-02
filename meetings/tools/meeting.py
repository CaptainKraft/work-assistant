#!/usr/bin/env python3
"""meeting.py - Craig multi-track meeting transcription pipeline.

Stages:
  ingest      Unzip a Craig multi-track download into a dated meeting folder.
  transcribe  Per-track speech-to-text with faster-whisper + VAD.
  merge       Combine per-track segments into one chronological transcript.
  all         ingest (if needed) -> transcribe -> merge.

Craig records one audio file per speaker, so each track is a single speaker
and attribution is exact - no diarization needed. The team-facing summary
(notes/summary.md) is written by the agent reading transcripts/combined.md,
not by this script. See meetings/AGENTS.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

# --- Layout ------------------------------------------------------------------

TOOLS_DIR = Path(__file__).resolve().parent
MEETINGS_ROOT = TOOLS_DIR.parent
PEOPLE_FILE = MEETINGS_ROOT / "people.json"
GLOSSARY_FILE = MEETINGS_ROOT / "glossary.md"

AUDIO_EXTS = {".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".opus", ".mp3"}
# Craig multi-track files look like "1-username.flac" or "12-some_name.wav".
TRACK_RE = re.compile(r"^(\d+)-(.+)$")
# Names that are mixdowns / non-speaker files, never treated as a track.
NON_TRACK_STEMS = {"combined", "mix", "mixed"}

DEFAULT_MODEL = "small.en"
DEFAULT_COMPUTE_TYPE = "int8"
COALESCE_GAP_SECONDS = 2.0


@dataclass
class Track:
    num: int
    username: str
    path: Path


# --- Helpers -----------------------------------------------------------------


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "meeting"


def fmt_ts(seconds: float) -> str:
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def is_track_name(stem: str) -> re.Match | None:
    m = TRACK_RE.match(stem)
    if not m:
        return None
    if stem.lower() in NON_TRACK_STEMS or m.group(2).lower() in NON_TRACK_STEMS:
        return None
    return m


def find_tracks(audio_dir: Path) -> list[Track]:
    tracks: list[Track] = []
    for p in sorted(audio_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXTS:
            continue
        m = is_track_name(p.stem)
        if not m:
            continue
        tracks.append(Track(num=int(m.group(1)), username=m.group(2), path=p))
    tracks.sort(key=lambda t: t.num)
    return tracks


def is_meeting_dir(p: Path) -> bool:
    return p.is_dir() and (p / "audio").is_dir()


def load_people() -> dict[str, str]:
    if not PEOPLE_FILE.exists():
        return {}
    try:
        data = json.loads(PEOPLE_FILE.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"error: {PEOPLE_FILE} is not valid JSON: {e}")
    return {str(k).lower(): str(v) for k, v in data.items() if v}


def display_name(username: str, people: dict[str, str]) -> str:
    return people.get(username.lower(), username)


def warn_unmapped(tracks: list[Track], people: dict[str, str]) -> None:
    unmapped = sorted({t.username for t in tracks if t.username.lower() not in people})
    if not unmapped:
        return
    print(f"note: {len(unmapped)} unmapped user(s) will show their Discord username:")
    for u in unmapped:
        print(f"  - {u}")
    print(f"  add real names to {PEOPLE_FILE}")


def load_glossary_terms() -> list[str]:
    """Canonical terms from glossary.md: the bolded entries in each ## section."""
    if not GLOSSARY_FILE.exists():
        return []
    terms: list[str] = []
    seen: set[str] = set()
    in_section = False
    for line in GLOSSARY_FILE.read_text().splitlines():
        if line.startswith("## "):
            in_section = True  # the intro is above the first heading and is skipped
            continue
        if not in_section or not line.lstrip().startswith("-"):
            continue
        for raw in re.findall(r"\*\*(.+?)\*\*", line):
            term = raw.strip().strip('"').strip()
            if not term or term.startswith("(") or "." in term:
                continue
            if term.lower() not in seen:
                seen.add(term.lower())
                terms.append(term)
    return terms


def build_initial_prompt(terms: list[str]) -> str | None:
    if not terms:
        return None
    return "JangaFX team meeting. Terms used include: " + ", ".join(terms) + "."


def resolve_meeting_dir(date_str: str | None, title: str | None) -> Path:
    date_str = date_str or date.today().isoformat()
    try:
        d = date.fromisoformat(date_str)
    except ValueError:
        sys.exit(f"error: --date must be YYYY-MM-DD, got {date_str!r}")
    name = f"{date_str}_{slugify(title)}" if title else date_str
    return MEETINGS_ROOT / f"{d.year:04d}" / name


# --- ingest ------------------------------------------------------------------


def _extract_zip_tracks(zip_path: Path, audio_dir: Path) -> int:
    count = 0
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            name = os.path.basename(member)
            if not name or os.path.splitext(name)[1].lower() not in AUDIO_EXTS:
                continue
            if not is_track_name(os.path.splitext(name)[0]):
                continue
            with z.open(member) as src, open(audio_dir / name, "wb") as dst:
                shutil.copyfileobj(src, dst)
            count += 1
    return count


def _copy_dir_tracks(src_dir: Path, audio_dir: Path) -> int:
    count = 0
    for p in sorted(src_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXTS:
            continue
        if not is_track_name(p.stem):
            continue
        target = audio_dir / p.name
        if p.resolve() != target.resolve():
            shutil.copy2(p, target)
        count += 1
    return count


def do_ingest(source: Path, date_str: str | None, title: str | None) -> Path:
    if not source.exists():
        sys.exit(f"error: source not found: {source}")
    meeting_dir = resolve_meeting_dir(date_str, title)
    audio_dir = meeting_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    (meeting_dir / "transcripts").mkdir(exist_ok=True)
    (meeting_dir / "notes").mkdir(exist_ok=True)

    if source.is_file() and source.suffix.lower() == ".zip":
        count = _extract_zip_tracks(source, audio_dir)
    elif source.is_dir():
        count = _copy_dir_tracks(source, audio_dir)
    else:
        sys.exit("error: source must be a Craig .zip or a directory of track files")

    if count == 0:
        sys.exit(f"error: no per-speaker tracks found in {source}")
    tracks = find_tracks(audio_dir)
    print(f"ingested {len(tracks)} tracks into {audio_dir}")
    for t in tracks:
        print(f"  {t.num:>3}  {t.path.name}")
    return meeting_dir


# --- transcribe --------------------------------------------------------------

_models: dict[tuple[str, str], object] = {}


def get_model(model_name: str, compute_type: str):
    key = (model_name, compute_type)
    if key not in _models:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            venv = TOOLS_DIR / ".venv"
            sys.exit(
                "error: faster-whisper is not installed.\n"
                f"  python3 -m venv {venv}\n"
                f"  {venv / 'bin' / 'pip'} install -r {TOOLS_DIR / 'requirements.txt'}\n"
                f"  then run: {TOOLS_DIR / 'meeting'} ..."
            )
        _models[key] = WhisperModel(model_name, device="cpu", compute_type=compute_type)
    return _models[key]


def transcribe_track(
    track: Track,
    model,
    model_name: str,
    language: str | None,
    initial_prompt: str | None,
    prompt_hash: str | None,
    tracks_dir: Path,
    force: bool,
) -> None:
    out = tracks_dir / f"{track.num}-{track.username}.json"
    if out.exists() and not force:
        cached = json.loads(out.read_text())
        fresh = out.stat().st_mtime >= track.path.stat().st_mtime
        if cached.get("model") == model_name and cached.get("prompt_hash") == prompt_hash and fresh:
            print(f"  skip  {track.path.name} (cached)")
            return

    segments, info = model.transcribe(
        str(track.path),
        language=language,
        initial_prompt=initial_prompt,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        beam_size=5,
    )
    segs = []
    for s in segments:
        text = s.text.strip()
        if text:
            segs.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": text})

    data = {
        "track": track.num,
        "username": track.username,
        "model": model_name,
        "prompt_hash": prompt_hash,
        "language": info.language,
        "duration": round(info.duration, 3),
        "segments": segs,
    }
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  done  {track.path.name} ({len(segs)} segments)")


def do_transcribe(
    meeting_dir: Path,
    model_name: str,
    language: str | None,
    compute_type: str,
    force: bool,
    use_glossary: bool = True,
) -> None:
    tracks = find_tracks(meeting_dir / "audio")
    if not tracks:
        sys.exit(f"error: no per-speaker tracks found in {meeting_dir / 'audio'}")
    tracks_dir = meeting_dir / "transcripts" / "tracks"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    warn_unmapped(tracks, load_people())

    terms = load_glossary_terms() if use_glossary else []
    initial_prompt = build_initial_prompt(terms)
    prompt_hash = hashlib.sha1(initial_prompt.encode()).hexdigest()[:12] if initial_prompt else None
    if initial_prompt:
        print(f"glossary: priming transcription with {len(terms)} terms from {GLOSSARY_FILE.name}")

    print(f"transcribing {len(tracks)} tracks with model '{model_name}' (lang={language or 'auto'}) ...")
    model = get_model(model_name, compute_type)
    for t in tracks:
        transcribe_track(t, model, model_name, language, initial_prompt, prompt_hash, tracks_dir, force)


# --- merge -------------------------------------------------------------------


def coalesce(segments: list[dict], max_gap: float = COALESCE_GAP_SECONDS) -> list[dict]:
    out: list[dict] = []
    for seg in segments:
        prev = out[-1] if out else None
        if prev and prev["username"] == seg["username"] and seg["start"] - prev["end"] <= max_gap:
            prev["end"] = seg["end"]
            prev["text"] = f"{prev['text']} {seg['text']}".strip()
        else:
            out.append(dict(seg))
    return out


def render_markdown(meeting_name: str, duration: float, attendees: dict[str, str], segments: list[dict]) -> str:
    names = ", ".join(sorted(set(attendees.values()), key=str.lower)) or "(none detected)"
    lines = [
        f"# {meeting_name}",
        "",
        f"- Duration: {fmt_ts(duration)}",
        f"- Attendees: {names}",
        "",
        "---",
        "",
    ]
    for s in segments:
        lines.append(f"[{fmt_ts(s['start'])}] **{s['speaker']}:** {s['text']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def do_merge(meeting_dir: Path) -> None:
    tracks_dir = meeting_dir / "transcripts" / "tracks"
    if not tracks_dir.is_dir():
        sys.exit(f"error: no transcripts/tracks in {meeting_dir} - run transcribe first")

    people = load_people()
    segments: list[dict] = []
    attendees: dict[str, str] = {}
    duration = 0.0

    for jf in sorted(tracks_dir.glob("*.json")):
        d = json.loads(jf.read_text())
        username = d["username"]
        name = display_name(username, people)
        duration = max(duration, d.get("duration", 0.0))
        for s in d["segments"]:
            segments.append(
                {"start": s["start"], "end": s["end"], "username": username, "speaker": name, "text": s["text"]}
            )
        if d["segments"]:
            attendees[username] = name

    segments.sort(key=lambda x: (x["start"], x["end"]))
    segments = coalesce(segments)

    transcripts = meeting_dir / "transcripts"
    combined = {
        "meeting": meeting_dir.name,
        "duration": round(duration, 3),
        "attendees": [{"username": u, "name": n} for u, n in sorted(attendees.items(), key=lambda kv: kv[1].lower())],
        "segments": segments,
    }
    (transcripts / "combined.json").write_text(json.dumps(combined, indent=2, ensure_ascii=False) + "\n")
    (transcripts / "combined.md").write_text(render_markdown(meeting_dir.name, duration, attendees, segments))
    print(f"merged {len(segments)} segments from {len(attendees)} speakers")
    print(f"  -> {transcripts / 'combined.md'}")
    print(f"  -> {transcripts / 'combined.json'}")


# --- CLI ---------------------------------------------------------------------


def add_model_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"faster-whisper model (default: {DEFAULT_MODEL}; e.g. medium.en for higher accuracy)")
    p.add_argument("--language", default="en", help="language code, or 'auto' to detect (default: en)")
    p.add_argument("--compute-type", default=DEFAULT_COMPUTE_TYPE,
                   help=f"CTranslate2 compute type (default: {DEFAULT_COMPUTE_TYPE})")
    p.add_argument("--force", action="store_true", help="re-transcribe even if a cached track JSON exists")
    p.add_argument("--no-glossary", action="store_true",
                   help="don't prime transcription with meetings/glossary.md terms")


def cmd_ingest(args: argparse.Namespace) -> None:
    do_ingest(Path(args.source).expanduser(), args.date, args.title)


def cmd_transcribe(args: argparse.Namespace) -> None:
    meeting_dir = Path(args.meeting_dir).expanduser()
    if not is_meeting_dir(meeting_dir):
        sys.exit(f"error: not a meeting folder (no audio/ inside): {meeting_dir}")
    language = None if args.language == "auto" else args.language
    do_transcribe(meeting_dir, args.model, language, args.compute_type, args.force, use_glossary=not args.no_glossary)


def cmd_merge(args: argparse.Namespace) -> None:
    meeting_dir = Path(args.meeting_dir).expanduser()
    if not meeting_dir.is_dir():
        sys.exit(f"error: meeting folder not found: {meeting_dir}")
    do_merge(meeting_dir)


def cmd_all(args: argparse.Namespace) -> None:
    source = Path(args.source).expanduser()
    if is_meeting_dir(source):
        meeting_dir = source
    else:
        meeting_dir = do_ingest(source, args.date, args.title)
    language = None if args.language == "auto" else args.language
    do_transcribe(meeting_dir, args.model, language, args.compute_type, args.force, use_glossary=not args.no_glossary)
    do_merge(meeting_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="meeting", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="unzip a Craig multi-track download into a dated meeting folder")
    p_ingest.add_argument("source", help="Craig .zip or a directory of track files")
    p_ingest.add_argument("--date", help="meeting date YYYY-MM-DD (default: today)")
    p_ingest.add_argument("--title", help="short meeting title used in the folder name")
    p_ingest.set_defaults(func=cmd_ingest)

    p_tr = sub.add_parser("transcribe", help="per-track speech-to-text with faster-whisper + VAD")
    p_tr.add_argument("meeting_dir", help="meeting folder (the one containing audio/)")
    add_model_args(p_tr)
    p_tr.set_defaults(func=cmd_transcribe)

    p_mg = sub.add_parser("merge", help="combine per-track segments into one transcript")
    p_mg.add_argument("meeting_dir", help="meeting folder (the one containing audio/)")
    p_mg.set_defaults(func=cmd_merge)

    p_all = sub.add_parser("all", help="ingest (if needed) -> transcribe -> merge")
    p_all.add_argument("source", help="Craig .zip, a directory of tracks, or an existing meeting folder")
    p_all.add_argument("--date", help="meeting date YYYY-MM-DD (default: today)")
    p_all.add_argument("--title", help="short meeting title used in the folder name")
    add_model_args(p_all)
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
