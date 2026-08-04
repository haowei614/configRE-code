# Ground-Truth Annotation — External Cases (EHR / Smart Grid / Loan Approval)

Thank you for helping validate the ground truth for this study. Your task is to
decide, **independently**, which quality dimensions (specialized agents) are
*relevant* for each of three software projects.

This is a **blinded** annotation: please base your judgement **only** on the
materials in this package. Do **not** look up the authors' own selections, any
automated tool output, or any scores — we want your independent expert opinion.

---

## What you receive

- `00_INSTRUCTIONS.md` — this file
- `AGENT_POOL.md` — definitions of the 15 quality agents
- `cases/EHR.md`, `cases/SmartGrid.md`, `cases/LoanApproval.md` — the three project descriptions
- `Annotation_Sheet.xlsx` — the spreadsheet you fill in (one tab per case)

## What "relevant" means

For each of the 15 agents, decide:

> Is this quality concern important enough that a **dedicated agent should
> reason about it and negotiate trade-offs** for *this* system?

- Mark **Y** (relevant) or **N** (not relevant) in the `Relevant (Y/N)` column.
- There is **no fixed number** of relevant agents. Typical systems need about
  **5–7**, but choose whatever the project actually warrants.
- Add a **one-line rationale** for each decision (why it is or isn't relevant).

## How to proceed

1. Read one case description in full (e.g. `cases/EHR.md`).
2. Open the matching tab in `Annotation_Sheet.xlsx` (e.g. the `EHR` tab).
3. Go through all 15 agents, filling `Relevant (Y/N)` and `Rationale`.
4. Repeat for the other two cases.
5. Fill in your annotator ID and date on the `README` tab, then send the file back.

## Ground rules

- Judge each case **on its own** — don't try to make cases consistent with each other.
- Judge each agent **on its own merits** — don't aim for a target count.
- If you're genuinely unsure, pick the closer option and note "borderline" in the rationale.
- Use only the project description + agent definitions; no external tools or the authors' answers.

Estimated effort: ~20–30 minutes per case (≈1–1.5 hours total).
