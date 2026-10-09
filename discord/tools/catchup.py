#!/usr/bin/env python3
"""catchup.py - pull recent Discord messages (read-only) for a catch-up summary.

Reads messages from the channels in the configured categories (see
discord/config.json) using the Kraftbot bot token stored in the macOS
Keychain, and writes one Markdown file per category:

  discord/<YYYY>/<start>_to_<end>/raw/<category>.md

The agent then reads those files and writes summary.md next to raw/.

Usage:
  discord/tools/catchup.py --since 14d
  discord/tools/catchup.py --since 2026-09-24 [--until 2026-10-01]
  discord/tools/catchup.py --since last          # from the end of the previous run
  discord/tools/catchup.py --since 3d --categories "Software Development"

Only GET requests are made. The bot never posts or changes anything.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://discord.com/api/v10"
DISCORD_EPOCH_MS = 1420070400000

DISCORD_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = DISCORD_DIR / "config.json"
STATE_PATH = DISCORD_DIR / ".state.json"
PEOPLE_PATH = DISCORD_DIR.parent / "meetings" / "people.json"

# Channel types: 0 text, 5 announcement, 15 forum. 4 is a category.
TEXT_TYPES = {0, 5}
FORUM_TYPE = 15
CATEGORY_TYPE = 4

# Message types worth reading: default, reply, slash command, context menu command.
CONTENT_MESSAGE_TYPES = {0, 19, 20, 23}


# --- API -------------------------------------------------------------------

def load_token(service):
    out = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-w"],
        capture_output=True, text=True,
    )
    token = out.stdout.strip()
    if out.returncode != 0 or not token:
        sys.exit(f"error: no Keychain item '{service}'. Add it with:\n"
                 f'  security add-generic-password -a "$USER" -s {service} -w')
    return token


class Api:
    def __init__(self, token):
        self.token = token
        self.calls = 0

    def get(self, path):
        """GET a path. Returns parsed JSON, or None on 403/404."""
        while True:
            req = urllib.request.Request(API + path, headers={
                "Authorization": "Bot " + self.token,
                "User-Agent": "DiscordBot (local-catchup, 0.1)",
            })
            self.calls += 1
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    data = json.load(r)
                    if r.headers.get("X-RateLimit-Remaining") == "0":
                        time.sleep(float(r.headers.get("X-RateLimit-Reset-After", "1")))
                    return data
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    body = json.loads(e.read() or b"{}")
                    time.sleep(float(body.get("retry_after", 1)) + 0.1)
                    continue
                if e.code in (403, 404):
                    return None
                raise


# --- Time / snowflakes -------------------------------------------------------

def snowflake_from_time(t):
    return (int(t.timestamp() * 1000) - DISCORD_EPOCH_MS) << 22


def time_from_snowflake(sf):
    return dt.datetime.fromtimestamp(((int(sf) >> 22) + DISCORD_EPOCH_MS) / 1000, dt.timezone.utc)


def parse_when(value, now):
    """'14d', '36h', 'YYYY-MM-DD', or an ISO timestamp -> aware datetime."""
    m = re.fullmatch(r"(\d+)([dh])", value)
    if m:
        n = int(m.group(1))
        return now - (dt.timedelta(days=n) if m.group(2) == "d" else dt.timedelta(hours=n))
    t = dt.datetime.fromisoformat(value)
    if t.tzinfo is None:
        t = t.astimezone()  # interpret as local time
    return t


# --- Fetching ----------------------------------------------------------------

def fetch_messages(api, channel_id, since_sf, until_sf):
    """All messages in [since, until), oldest first. Pages backwards with `before`."""
    out = []
    before = until_sf
    while True:
        batch = api.get(f"/channels/{channel_id}/messages?limit=100&before={before}")
        if not batch:
            break
        for m in batch:
            if int(m["id"]) > since_sf:
                out.append(m)
        oldest = min(int(m["id"]) for m in batch)
        if oldest <= since_sf or len(batch) < 100:
            break
        before = oldest
    out.sort(key=lambda m: int(m["id"]))
    return out


def fetch_archived_threads(api, channel_id, since):
    """Public archived threads under a channel, archived at or after `since`."""
    threads = []
    before = None
    while True:
        q = "?limit=100" + (f"&before={before}" if before else "")
        page = api.get(f"/channels/{channel_id}/threads/archived/public{q}")
        if not page or not page.get("threads"):
            break
        done = False
        for t in page["threads"]:
            archived_at = dt.datetime.fromisoformat(t["thread_metadata"]["archive_timestamp"])
            if archived_at < since:
                done = True
                break
            threads.append(t)
        if done or not page.get("has_more"):
            break
        before = page["threads"][-1]["thread_metadata"]["archive_timestamp"]
    return threads


# --- Formatting ----------------------------------------------------------------

class Names:
    def __init__(self, people):
        self.people = people

    def of(self, user):
        uname = (user.get("username") or "").lower()
        if uname in self.people:
            return self.people[uname]
        return user.get("global_name") or user.get("username") or "unknown"


def clean_content(m, names, channel_names, role_names):
    text = m.get("content") or ""
    for u in m.get("mentions", []):
        text = re.sub(rf"<@!?{u['id']}>", "@" + names.of(u), text)
    text = re.sub(r"<#(\d+)>", lambda x: "#" + channel_names.get(x.group(1), "channel"), text)
    text = re.sub(r"<@&(\d+)>", lambda x: "@" + role_names.get(x.group(1), "role"), text)
    text = re.sub(r"<a?(:\w+:)\d+>", r"\1", text)
    text = re.sub(r"<t:(\d+)(?::\w)?>",
                  lambda x: dt.datetime.fromtimestamp(int(x.group(1))).strftime("%Y-%m-%d %H:%M"), text)
    return text


def format_message(m, names, channel_names, role_names):
    when = dt.datetime.fromisoformat(m["timestamp"]).astimezone().strftime("%m-%d %H:%M")
    who = names.of(m["author"])
    if m["author"].get("bot"):
        who += " [bot]"

    head = f"[{when}] **{who}**"
    ref = m.get("referenced_message")
    if ref:
        snippet = clean_content(ref, names, channel_names, role_names).replace("\n", " ")
        if len(snippet) > 80:
            snippet = snippet[:77] + "..."
        head += f' (reply to {names.of(ref["author"])}: "{snippet}")'

    body = clean_content(m, names, channel_names, role_names)
    extras = []
    for a in m.get("attachments", []):
        extras.append(f"[attachment: {a.get('filename', 'file')}]")
    for e in m.get("embeds", []):
        bits = [e.get("title"), e.get("description")]
        bits = [b for b in bits if b]
        if bits and not body:
            desc = " - ".join(bits).replace("\n", " ")
            extras.append(f"[embed: {desc[:300]}]")
        elif e.get("url") and e.get("title"):
            extras.append(f"[link: {e['title']}]")
    for s in m.get("sticker_items", []):
        extras.append(f"[sticker: {s.get('name')}]")
    if m.get("poll"):
        extras.append(f"[poll: {m['poll'].get('question', {}).get('text', '')}]")

    full = " ".join([p for p in [body] + extras if p])
    lines = full.split("\n")
    out = f"{head}: {lines[0]}"
    for line in lines[1:]:
        out += "\n    " + line
    return out


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# --- Main ---------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Pull recent Discord messages for a catch-up summary (read-only).")
    p.add_argument("--since", required=True, help="'14d', '36h', 'YYYY-MM-DD', ISO time, or 'last'")
    p.add_argument("--until", help="end of window (default: now); same formats as --since")
    p.add_argument("--categories", nargs="+", help="override category names from config.json")
    p.add_argument("--out", help="output folder (default: discord/<YYYY>/<start>_to_<end>)")
    args = p.parse_args()

    config = json.loads(CONFIG_PATH.read_text())
    people = json.loads(PEOPLE_PATH.read_text()) if PEOPLE_PATH.exists() else {}
    names = Names({k.lower(): v for k, v in people.items()})

    now = dt.datetime.now(dt.timezone.utc)
    if args.since == "last":
        if not STATE_PATH.exists():
            sys.exit("error: no previous run recorded; pass --since 14d or a date")
        since = dt.datetime.fromisoformat(json.loads(STATE_PATH.read_text())["last_until"])
    else:
        since = parse_when(args.since, now)
    until = parse_when(args.until, now) if args.until else now
    since_sf, until_sf = snowflake_from_time(since), snowflake_from_time(until)

    wanted = [c.lower() for c in (args.categories or config["categories"])]

    api = Api(load_token(config["keychain_service"]))
    gid = config["guild_id"]

    channels = api.get(f"/guilds/{gid}/channels") or sys.exit("error: cannot list guild channels")
    roles = api.get(f"/guilds/{gid}/roles") or []
    role_names = {r["id"]: r["name"] for r in roles}
    channel_names = {c["id"]: c["name"] for c in channels}
    categories = {c["id"]: c for c in channels if c["type"] == CATEGORY_TYPE}

    missing = set(wanted) - {c["name"].lower() for c in categories.values()}
    if missing:
        print(f"warning: no category named: {', '.join(sorted(missing))}", file=sys.stderr)

    selected = {}  # category name -> [channels]
    for cat in sorted(categories.values(), key=lambda c: c["position"]):
        if cat["name"].lower() not in wanted:
            continue
        kids = [c for c in channels
                if c.get("parent_id") == cat["id"] and (c["type"] in TEXT_TYPES or c["type"] == FORUM_TYPE)]
        selected[cat["name"]] = sorted(kids, key=lambda c: c["position"])

    parent_ids = {c["id"] for kids in selected.values() for c in kids}
    active = (api.get(f"/guilds/{gid}/threads/active") or {}).get("threads", [])
    threads_by_parent = {}
    for t in active:
        if t.get("parent_id") in parent_ids:
            threads_by_parent.setdefault(t["parent_id"], {})[t["id"]] = t

    local_since = since.astimezone()
    local_until = until.astimezone()
    out_dir = Path(args.out) if args.out else (
        DISCORD_DIR / f"{local_since:%Y}" / f"{local_since:%Y-%m-%d}_to_{local_until:%Y-%m-%d}")
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    totals = []
    for cat_name, kids in selected.items():
        sections = []
        cat_count = 0
        for ch in kids:
            for t in fetch_archived_threads(api, ch["id"], since):
                threads_by_parent.setdefault(ch["id"], {})[t["id"]] = t

            parts = []
            n = 0
            if ch["type"] in TEXT_TYPES:
                msgs = [m for m in fetch_messages(api, ch["id"], since_sf, until_sf)
                        if m.get("type") in CONTENT_MESSAGE_TYPES]
                if msgs:
                    parts.append("\n".join(format_message(m, names, channel_names, role_names) for m in msgs))
                    n += len(msgs)

            threads = sorted(threads_by_parent.get(ch["id"], {}).values(), key=lambda t: int(t["id"]))
            for t in threads:
                last = t.get("last_message_id")
                if not last or int(last) <= since_sf:
                    continue
                msgs = [m for m in fetch_messages(api, t["id"], since_sf, until_sf)
                        if m.get("type") in CONTENT_MESSAGE_TYPES]
                if not msgs:
                    continue
                started = time_from_snowflake(t["id"]).astimezone()
                label = "Post" if ch["type"] == FORUM_TYPE else "Thread"
                note = "" if started >= local_since else f" (started {started:%Y-%m-%d}, earlier messages not included)"
                parts.append(f"#### {label}: {t['name']}{note}\n\n" +
                             "\n".join(format_message(m, names, channel_names, role_names) for m in msgs))
                n += len(msgs)

            if n:
                sections.append(f"### #{ch['name']} ({n} messages)\n\n" + "\n\n".join(parts))
                cat_count += n
            print(f"  {cat_name} / #{ch['name']}: {n}", file=sys.stderr)

        header = (f"# {cat_name}\n\n"
                  f"- Server: {config['guild_name']}\n"
                  f"- Window: {local_since:%Y-%m-%d %H:%M} to {local_until:%Y-%m-%d %H:%M} (local time)\n"
                  f"- Messages: {cat_count}\n")
        body = "\n\n".join(sections) if sections else "_No messages in this window._"
        (raw_dir / f"{slugify(cat_name)}.md").write_text(header + "\n" + body + "\n")
        totals.append((cat_name, cat_count))

    # Only "up to now" runs move the marker; a past window shouldn't reset it.
    if not args.until:
        STATE_PATH.write_text(json.dumps({"last_until": until.isoformat()}, indent=2) + "\n")

    print(f"\nWrote {raw_dir}  ({api.calls} API calls)")
    for name, n in totals:
        print(f"  {n:5d}  {name}")


if __name__ == "__main__":
    main()
