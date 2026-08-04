# Human Evaluation Package — Downstream Requirements Quality

## What this is
Blinded requirement specifications produced by 4 (undisclosed) configuration
processes across 4 case studies: EHR, SmartGrid, LoanApproval, W-Mobility.
Total: 16 documents (4 cases x 4 configs).

## For evaluators
1. Read `RUBRIC.md` (4 dimensions, Likert 1-5).
2. For each case folder, first read `00_PROJECT_DESCRIPTION.md`.
3. Then read each `<CASE>-<LETTER>.md` requirement set and score it.
4. Fill in a COPY of `scoring_sheet_TEMPLATE.csv` (put your name in `evaluator_id`).
   Do NOT try to guess which method produced which document.

## For the researcher (you)
- `DECODE_MAP_researcher_only.csv` maps each blind label -> real configuration.
  Do NOT share this with evaluators.
- After collecting all evaluators' sheets, run:
      python merge_human_eval_scores.py
  which decodes blind labels to configs and writes
  `configRE-code/experiments/results/human_evaluation_scores.csv`
  in the exact format expected by `analyze_human_evaluation.py`.
- Then:
      cd configRE-code && python experiments/analyze_human_evaluation.py
  to produce the aggregated table + Krippendorff's alpha + LaTeX.

## Config mapping (secret)
Standard cases: config_a=Fixed-5, config_b=Domain-opt, config_c=Full-15, config_d=Phase0-Auto
W-Mobility (Aisin): fixed5=Fixed-5, domainopt=Domain-opt, full15=Full-15, auto=Phase0-Auto
See DECODE_MAP_researcher_only.csv for the authoritative per-document mapping.
