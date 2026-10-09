# Agent Instructions (Discord catch-up)

This directory pulls recent messages from the **JangaFX Dev Team** Discord server and turns them
into a catch-up summary for Jeremiah.

Access is through **Kraftbot**, Jeremiah's personal bot (separate from any JangaFX bot). Its token
lives in the macOS Keychain under the service name `discord-bot-token`.

## Safety / constraints

- Read-only. The tool only makes GET requests. Never post, react, or change anything on Discord.
- Never print, log, or paste the token. Read it from Keychain inside the script only.
- Raw message dumps stay local (gitignored). Only `summary.md` is tracked.

## Config (`discord/config.json`)

- `categories`: which server sections to read. Defaults: Operations, JangaFX HQ, Software
  Development, Other Development.
- `guild_id`, `keychain_service`: rarely change.

Display names come from `meetings/people.json` (Discord username → name), shared with the
meetings pipeline. Unmapped users show their Discord display name.

## Running

```bash
discord/tools/catchup.py --since 14d              # last 14 days
discord/tools/catchup.py --since 2026-09-24       # since a date (local time)
discord/tools/catchup.py --since last             # since the end of the previous run
discord/tools/catchup.py --since 3d --categories "Software Development"
```

`--until` sets an end other than now. Runs that end at "now" update the `last` marker
(`discord/.state.json`); runs with `--until` don't.

Output:

```
discord/<YYYY>/<start>_to_<end>/
  raw/<category>.md   # every message, grouped by channel, threads/forum posts included
  summary.md          # written by the agent
```

## Writing the summary

1. Read every file in `raw/`. For big windows, split by category and summarize each, then merge.
2. Write `summary.md` with these sections:
   - **Needs your attention**: decisions waiting, blockers, things that involve Jeremiah directly,
     process gaps, deadlines, and friction between people.
   - One section per product/area (EmberGen 2, IlluGen, LiquiGen, shared tech, business).
   - **People**: births, sick days, travel, time off.
3. Lead with what matters to a manager. Skip banter and social channels unless something real is
   in there (team news, complaints about process or tools).
4. Be faithful. Don't invent decisions. Say "no decision yet" when something is open.
5. Write PR/issue references as `jangafx/EmberGen#NNNN`.
6. Plain words, short sentences.
