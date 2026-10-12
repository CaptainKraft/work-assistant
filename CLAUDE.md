@AGENTS.md

# JangaFX cycle process (Nick, 2026-10-12)

On 2026-10-12 Nick announced the end of JangaFX's flat structure. Jeremiah is now **Product Manager** and owns the cycle board, so most of this process runs through him. The full post is in [process/2026-10-12-nick-cycle-process-announcement.md](process/2026-10-12-nick-cycle-process-announcement.md), and Jeremiah's one-page quick reference is in [process/jeremiah-quick-reference.md](process/jeremiah-quick-reference.md). Read it before helping with cycle planning, standups, scope calls, PR or QA policy, or team communication about any of these.

## Timeline and scope

- **In full effect:** 2027-01-04, the next full cycle. Until then, apply as much as possible to the current cycle.
- **Rollout:** EmberGen 2 first (flagship, needs time allocations now), then the other products.
- **Cycle:** 6 weeks, fixed once Phase 5 greenlights it. Every programmer has assigned work for every day.

## Hierarchy

Nick → **Jeremiah (Product Manager)** → Product Leads → Programming team

| Product | Lead |
|---|---|
| EmberGen (EG) | Morten |
| IlluGen (IG) | Gil |
| LiquiGen (LG) | Javier |
| Web | Mihai |

- Product leads have the final say on *how* something gets built in their product.
- Programmers own their tasks and the implementation. They go to their lead when they need a decision made.
- The artist council (Sebastien, Jason, Daniel, Shirk) votes on feature order.

## Cooldown

Each cooldown costs about **$141,000**, so it is no longer free time. Cooldown is only for:

- backlog bug fixes
- helping teammates finish cycle tasks
- scope planning for larger tasks
- final QA before releases
- planning the next cycle (below)

## Planning phases (run during cooldown)

1. **Carry-over.** Unfinished items from the last cycle carry over. Keep this list short; cooldown should finish most of them.
2. **Artist feature call.** Artists, Nick and Jeremiah meet once per art product (EG, IG, LG). They vote on feature requests backed by real artistic need, ranked by importance to studios and customers.
3. **Product lead calls.** Each lead gets their own call to review the combined task list and assigned programmers. Leads can reassign people, add tasks and triage the artist list. Technical items (debt, performance, crashes) enter here through the lead.
4. **Dev estimates.** Programmers estimate their own tasks throughout planning.
5. **Final overview.** Nick and Jeremiah settle disagreements and greenlight the cycle. After this the cycle is fixed.

## Rules for programmers (what Jeremiah enforces)

1. **Daily written standup:** what you're working on and whether you're on track. Jeremiah keeps the board current from these. Mark a task done and get its PR merged before starting the next one.
2. **Only board work.** Every task must be named, have time allocated and be in the cycle milestone. Anything else needs Jeremiah's approval. Programmers must report when they're working on something that has no item.
   - **Cycle-breaking** means only a serious bug that completely stops a live studio customer from finishing a production (for example imports or exports). A feature request is never cycle-breaking. Jeremiah approves cycle-breaking work before it starts.
3. **Programmers write their own estimates** before the cycle starts.
4. **150% rule.** At 150% of the estimate, work stops. The team then ships as is, re-scopes or kills the feature, and **the decision is recorded**. Going over isn't a failure; not reporting it is.
5. **PRs:** no PR sits longer than 24 hours. Mandatory peer review is gone. Claude reviews every PR, then the author merges it. The author owns the code and any fallout.
6. **All requests go through intake.** Nobody builds something because they were asked directly, even by Nick. Every request goes through intake at cycle planning.
7. **Meetings are mandatory.** Weekly dev team meetings, starting with EmberGen 2.
8. **Authors QA their own features**, before and after merging, using PUP (and possibly a future Claude MCP). Ask an artist for more testing. Programmers no longer QA other tools, and the QA teams will be phased out to some degree (details TBD).

## How to apply this when helping Jeremiah

- **The cycle milestone in git is the system of record.** Treat anything outside it as unapproved unless Jeremiah approved it. When summarizing GitHub activity (`gh/`), Discord (`discord/`) or meetings (`meetings/`), flag:
  - work with no milestone item
  - PRs open longer than 24h, or merged without a Claude review
  - tasks near or over 150% of their estimate
  - feature requests sent straight to programmers instead of through intake
  - missing standups
- **Standups → board.** Turning written standups into board updates is a daily job for Jeremiah. Help with it, and show slips against estimates.
- **150% decisions get written down:** task, estimate, actual time, decision (ship / re-scope / kill), who decided and why.
- **Cycle planning work** (`priorities/`) should follow the five phases above and produce a final cycle with an owner, an estimate and a milestone entry for every task.
- **Tone with the team:** Nick's framing is cost and accountability. Jeremiah frames it as clear goals and boundaries rather than authority (see the dev-ops memory). Draft team-facing messages in that spirit.
