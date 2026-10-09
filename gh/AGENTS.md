# Agent Instructions (GitHub / `gh` workflow)

This directory is for read-only GitHub reporting workflows using GitHub CLI (`gh`).

## Defaults

- Default repo: `jangafx/embergen`
- Default stale threshold: **14 days** (based on last activity / `updatedAt`)
- Default report output dir: `gh/reports/`
- Default report file: `gh/reports/stale-prs-embergen.md`

If the user explicitly provides a different repo or threshold, follow the user.

## Safety / constraints

- Read-only GitHub operations only unless the user explicitly requests write actions.
- Exception: the "Notification inbox walkthrough" marks notifications Done (`DELETE /notifications/threads/{id}`). Only ever do this per item, in direct response to an explicit user action (a clicked button or typed instruction) — never bulk-mark or auto-mark.
- Do not clone repos.
- Do not access local repo working copies.
- Always target repos using `-R owner/repo` (never rely on `gh repo set-default`).
- Never request, print, or paste tokens/keys. Authentication should be done via `gh auth login` on the user’s machine.

## Name mapping (GitHub login → display name)

- `rxi` → Mike
- `AquaGeneral` → Jesse
- `gingerBill` → Bill
- `Said6289` → Said
- `AlvaroFS` → Alvaro
- `graphitemaster` → Dale

If a PR author is not in this mapping, display their GitHub login, and ask what name the login should map to.

## “Stale PR summary” definition

When the user asks for a stale PR summary (or similar wording), generate a Discord-ready Markdown report:

1. Fetch all **open, non-draft** PRs for the target repo.
   - Use `gh pr list` with `--state open` and `--search "draft:false"`.
   - Fetch JSON fields at least: `number,title,url,author,createdAt,updatedAt`.

2. Filter to PRs whose **last activity** is at least N days ago.
   - `last activity` is derived from `updatedAt`.
   - Default N = 14 unless user overrides.

3. Group PRs by author (using mapping above) and order PRs **oldest → newest** within each author group (by `createdAt`).
   - Order author groups by the createdAt of their oldest PR (oldest author-group first).

4. Determine merge conflicts **definitively** for each included PR.
   - GitHub may initially return unknown mergeability.
   - Poll per-PR using: `gh api repos/{owner}/{repo}/pulls/{number}` until mergeability is computed.
   - Treat `mergeable_state == "dirty"` as **merge conflicts**.

5. Output format (Discord-ready Markdown)

- Header:
  - `**Stale open PRs (non-draft)**` and a line describing the filter used.
- For each author section:
  - `**<Name>**`
- For each PR bullet:
  - `- [#<num> <title>](<url>)`
  - Sub-bullets:
    - `created: X days ago`
    - `last activity: Y days ago`
    - Only if applicable: `merge conflicts`

6. Save output to a Markdown file in `gh/reports/`.
   - Default: `gh/reports/stale-prs-embergen.md`.
   - If repo/threshold overridden, choose a sensible filename (e.g. `gh/reports/stale-prs-<owner>-<repo>.md`).

## “Notification inbox walkthrough” definition

When the user asks to go through their GitHub notifications / inbox (e.g. "walk my notifications", "go through my inbox one by one"), step through unresolved notifications **oldest → newest, one at a time**, summarizing each and letting the user mark it Done or skip.

### Write exception
This is the one workflow here that performs **writes**: marking a notification Done is `DELETE /notifications/threads/{id}`. Only mark Done in response to an explicit per-item user action. Never bulk-mark or auto-mark, and never mark something Done that the user told you to skip.

### 1. Fetch the inbox (oldest → newest)
- `gh api "/notifications?all=true" --paginate` — **`all=true` is required.** The default returns only *unread* threads and silently hides notifications you've already opened but not finished. `all=true` returns read + unread and excludes only those already marked Done. State the total count up front.
- Capture per thread at least: `.id` (thread id — needed to mark Done), `.unread`, `.subject.type`, `.subject.url`, `.subject.title`, `.updated_at`.
- Sort ascending by `.updated_at`. Don't assume the unread set is the whole inbox — already-read-but-not-Done items are usually the *oldest* and easy to miss.
- Notifications span all repos by default; if the user names a repo, filter on `.repository.full_name`.

```
gh api "/notifications?all=true" --paginate \
  --jq 'sort_by(.updated_at) | .[] | [.id, .updated_at, (if .unread then "UNREAD" else "read" end), .subject.type, .subject.url, .subject.title] | @tsv'
```

### 2. Per-item detail
Fetch detail so the summary is real, not just the title:
- Pull request: `gh pr view <n> -R <owner/repo> --json number,title,state,isDraft,baseRefName,headRefName,author,createdAt,mergedAt,additions,deletions,changedFiles,comments,body`
  - Always include and report **`baseRefName`** (branch it targets / merged into). See branch flagging below.
- Issue: `gh issue view <n> -R <owner/repo> --json number,title,state,author,createdAt,labels,comments,body`
  - Include the **latest comment** — it's usually *why* the notification fired.

### 3. Summary format (one per notification)
- Position + read state: `N of TOTAL`, and whether it's UNREAD or already-read.
- Title as a **clickable markdown link** to the PR/issue.
- Status line: merged / open / closed / draft · **base branch** · author (via the login→name mapping above; show the login if unmapped) · merge/created date · size (files, +/−) · comment count.
- 1–4 bullets on what it does (from the body); for issues, a bullet on *why it pinged you* (latest comment).
- Any flags (below), called out prominently.

### Branch flagging (matters at release time)
- `development` is the default integration branch — just state it, no flag.
- Release branches follow `release-<year>-cycle<N>` (plus `-patch<M>` and IG-specific patch variants), e.g. `release-2026-cycle3`. **Flag prominently (🚨)** any PR merged into / targeting a `release-*` branch — these are what the user watches near release.
- A PR from `release-*` → `development` is a **forward-port** keeping dev in sync — note it as such (often a near-duplicate title of a release-branch PR).

### Things to flag
- **Closed without merging** (state closed, not merged) — may be superseded; offer to find the replacement PR.
- **Secrets in the body** (tokens, client secrets, API keys) — flag 🔐 and suggest rotation, even if labeled "temporary".
- **Drafts**, and **dependency notes** ("merge #X first").
- Bug/issue reports that look related to a change elsewhere in the same batch.

### 4. Interaction (one at a time)
After each summary, offer exactly **two actions** and wait:
- **Mark done & next** → mark the current thread Done, then summarize the next.
- **Skip & next** → leave it in the inbox, then summarize the next.

If the client supports inline interactive widgets (e.g. Claude Code's `show_widget` + `sendPrompt`), render these as **two compact buttons** in a single short row — no third "Other"/free-text option, since a tall popup obstructs the reading area. Buttons send the plain phrases `mark done, go next` / `skip (do not mark done), go next`. Otherwise present the two options as text. The user may also type a free-form question about the current item at any time — answer it, then re-offer the two actions.

Mark Done (reuse the `.id` captured in step 1, or resolve it):
```
tid=$(gh api "/notifications?all=true" --paginate --jq '.[] | select(.subject.url|endswith("/<pulls|issues>/<n>")) | .id')
gh api --method DELETE "/notifications/threads/$tid"
```

### 5. Wrap-up
When the list is exhausted, output a **table of what's left** in the inbox (the skipped items): number + link, type, title, open/closed state, and a one-line note. That table is the user's residual to-do list.

## Example invocations

Use natural language; the agent should apply defaults unless overridden.

- `stale PR summary`
- `stale PR summary for jangafx/embergen`
- `stale PR summary for owner/repo` (override repo)
- `stale PR summary, threshold 30 days` (override threshold)
- `stale PR summary for owner/repo, threshold 30 days` (override both)
- `walk my GitHub notifications` / `go through my inbox one by one`
- `go through my notifications, oldest first`

## Quick troubleshooting

- If `gh auth status -h github.com` shows not logged in: user should run `gh auth login -h github.com -p https`.
- If mergeability keeps coming back unknown: keep polling a few times with small delay.
- If notifications you've already opened don't show up in the walkthrough: you forgot `all=true` (the default lists unread only). Threads already marked Done never reappear, even with `all=true`.
