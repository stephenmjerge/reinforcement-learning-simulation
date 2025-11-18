# Issues

Capture research ideas and bugs in the shared GitHub project, then mirror high-priority tasks inside `meta/launchpad/next-actions.md`. Each issue should specify:

- Environment file(s) affected.
- Baselines or metrics that regressed.
- Safety considerations to review with the ethics lead.

## Issue: Implement second reward schedule
- Source: `meta/launchpad/next-actions.md` (RL-Sim section)
- Acceptance criteria:
  - Stable and volatile schedules live in code with docstring example.
  - Simple simulation helper exposes rewards for plotting.
  - Roadmap + changelog updated so the milestone is traceable.
- Status: Completed (Nov 13, 2025).

## Issue: Run simulation for low vs high severity groups
- Source: `meta/launchpad/next-actions.md` (RL-Sim section)
- Acceptance criteria:
  - Severity helper exposes default profiles (low vs. high) plus summary stats.
  - README documents how to call the helper inside notebooks.
  - Roadmap/next-actions updated once the helper lands.
- Status: Completed (Nov 13, 2025).

## Issue: Sketch 1–2 figures for simulation paper
- Source: `meta/launchpad/next-actions.md` (RL-Sim section)
- Acceptance criteria:
  - Provide at least one runnable script that outputs a PNG comparing low vs. high severity groups.
  - Document the figure concept(s) in `docs/figures.md` plus a README blurb so collaborators can reproduce it.
  - Mark the `meta/launchpad` checklist item complete once the assets exist.
- Status: Completed (Nov 13, 2025).
