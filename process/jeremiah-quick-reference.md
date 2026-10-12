# Cycle process: Jeremiah's quick reference

Source: [Nick's announcement, 2026-10-12](2026-10-12-nick-cycle-process-announcement.md). There's a longer summary in the root [CLAUDE.md](../CLAUDE.md).

## Your role: Product Manager

**Nick → Jeremiah → Product Leads (Morten EG, Gil IG, Javier LG, Mihai web) → programmers**

- **Timing:** the process is fully in place from **2027-01-04**. Apply what you can to the current cycle now.
- **Rollout:** EmberGen 2 first, then the other products.

## Cycle shape

- **6-week cycle.** It's fixed once you and Nick greenlight it, and every programmer has assigned work every day.
- **Cooldown:** costs about $141k each time, so it's no longer free time. It's for:
  - backlog bugs
  - helping teammates finish
  - scoping large tasks
  - final QA before release
  - planning the next cycle

## Planning during cooldown

You're in phases 2, 4 and 5, and you own the result.

1. **Carry-over:** unfinished items roll into the next cycle. Keep this list short.
2. **Artist feature call:** you, Nick and the artists (Sebastien, Jason, Daniel, Shirk), once each for EG, IG and LG. The artists vote features in order of importance.
3. **Lead calls:** each product lead reviews the combined task list and who's assigned. They can reassign people, add tech items (debt, performance, crashes) and triage the artist list.
4. **Dev estimates:** programmers estimate their own tasks throughout planning.
5. **Final overview with Nick:** settle disagreements and greenlight the cycle.

## Your daily and weekly duties

- **Read the daily written standups** and update the board from them. The board should be accurate to the day.
- **Approve or deny work that isn't on the board.** Every task must be named, have time allocated and sit in the cycle milestone.
- **Approve cycle-breaking work before it starts.** Only a serious bug that stops a live studio's production qualifies, such as imports or exports. A feature request never does.
- **Enforce the 150% rule.** At 150% of the estimate, work stops and the team ships as is, re-scopes or kills the feature. **Record the decision.** Going over isn't a failure; not reporting it is.
- **Weekly dev meetings** are mandatory, starting with EmberGen 2.

## Rules to watch for

| Rule | What to look for |
|---|---|
| Tasks finished in order | Task marked done and its PR merged before the next one starts |
| PRs | Open no longer than 24h; Claude review required, no peer review |
| Intake only | Nobody builds something because they were asked directly, even by Nick |
| QA | Authors QA their own features before and after merging (PUP, artists); no QA of other tools |
| Ownership | The programmer owns the implementation; the product lead has final say on how |

## Open items

- QA team phase-out: details still to come.
- Which tool is the board? Probably the GitHub milestone. The priorities tool's goals currently rule out sprint and board features.
