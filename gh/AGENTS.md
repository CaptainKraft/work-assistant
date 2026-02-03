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

## Example invocations

Use natural language; the agent should apply defaults unless overridden.

- `stale PR summary`
- `stale PR summary for jangafx/embergen`
- `stale PR summary for owner/repo` (override repo)
- `stale PR summary, threshold 30 days` (override threshold)
- `stale PR summary for owner/repo, threshold 30 days` (override both)

## Quick troubleshooting

- If `gh auth status -h github.com` shows not logged in: user should run `gh auth login -h github.com -p https`.
- If mergeability keeps coming back unknown: keep polling a few times with small delay.
